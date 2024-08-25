import flet as ft

import math

from .ndcss import *
from .edge import Edge
from .items import *

class data_param():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class NodeEvent():
    def __init__(self, src_node, target_node, src_item_id, target_item_id) -> None:
        self.src_node = src_node
        self.target_node = target_node
        self.src_item_id = src_item_id
        self.target_item_id = target_item_id

class Node(ft.GestureDetector):
    def __init__(self, width, height, top, left, edge, style={}):
        super().__init__()
        self.main_content = ft.Ref[ft.Column()]
        self.edge = edge
        
        self.ndcss = style

        self.target_node = None
        self.callback_handler = None
        self.inputs = []
        self.outputs = []
        self.next_obj_left = 0
        self.next_obj_top = 30
        self.node_width = width
        self.node_height = height
        self.inout_point_diameter = 10
        self.disp_obj_offset = self.inout_point_diameter/2
        self.obj_width = self.node_width - self.inout_point_diameter
        self.obj_height = 20
        

        self.mouse_cursor = ft.MouseCursor.CLICK
        self.on_pan_update = self.drag
        self.drag_interval = 5
        self.top = top
        self.left = left
        
        node_style=self.ndcss.get("node", {})

        self.content = ft.Container(
            **(self.ndcss.get("node_brim", {})),
            width=self.node_width,
            height=self.node_height,
            border_radius= ft.border_radius.all(6),
            content=ft.Stack(
                [
                    ft.Container(
                        key="info",
                        border_radius= ft.border_radius.all(6),
                        border=ft.border.all(node_style.get("border_width"), node_style.get("border_color")),
                        bgcolor=node_style.get("bgcolor"),
                        width=self.obj_width,
                        height=self.node_height,
                        left=self.disp_obj_offset,
                    ),
                ],
                ref=self.main_content,
            ),
        )

    def drag(self, e: ft.DragUpdateEvent):
       e.control.top = max(0, e.control.top + e.delta_y)
       e.control.left = max(0, e.control.left + e.delta_x)
       e.control.update()
       self.re_draw_connection(e)

    def re_draw_connection(self, e):
        stack_obj = e.control.content.content
        for n in stack_obj.controls:
            if(n.key == "obj"):
                self.edge.update_edge(e.control, n.data.id , n.data.x + e.control.left, n.data.y + e.control.top)

    def connect(self, target_node):
        self.target_node = target_node
        draw_len_x = self.left - self.target_node.left
        draw_len_y = self.top - self.target_node.top
        draw_len = math.sqrt(draw_len_x**2 + draw_len_y**2)

    def register_callback(self, callback):
        self.callback_handler = callback

    def append_header(self, text=None):
        view = Item_Header(self, text=text, style=self.ndcss.get("Item_Header", {}))
        self.content.content.controls.append(view)

    def append_output(self, id, text=None):
        output_pointer_pos_x = self.next_obj_left + self.node_width - self.inout_point_diameter/2
        output_pointer_pos_y = self.next_obj_top + self.inout_point_diameter/2
        m_data_param = data_param(id, output_pointer_pos_x, output_pointer_pos_y)
    
        view = Item_Interface_IN(
                                    id,
                                    self,
                                    data=m_data_param,
                                    left=self.next_obj_left,
                                    top=self.next_obj_top,
                                    text=text,
                                    style=self.ndcss.get("Item_Interface_IN", {})
                                 )

        self.next_obj_top += self.obj_height
        
        self.content.content.controls.append(view)

        self.outputs.append(id)

    def append_input(self, id, text=None):
        output_pointer_pos_x = self.next_obj_left + self.inout_point_diameter/2
        output_pointer_pos_y = self.next_obj_top + self.inout_point_diameter/2
        m_data_param = data_param(id, output_pointer_pos_x, output_pointer_pos_y)

        view = Item_Interface_OUT(
                                    id,
                                    self,
                                    data=m_data_param,
                                    left=self.next_obj_left,
                                    top=self.next_obj_top,
                                    text=text,
                                    style=self.ndcss.get("Item_Interface_OUT", {})
                                 )

        self.next_obj_top += self.obj_height
        
        self.content.content.controls.append(view)
        
        self.inputs.append(id)


    def drag_will_accept(self, e):
        
        e.control.update()

    def drag_accept(self, e: ft.DragTargetAcceptEvent):
        src = self.page.get_control(e.src_id)

        src_node = src.content.parent.parent.parent.parent.parent.parent
        target_node = e.control.parent.parent.parent.parent.parent

        src_node_item = src.content.parent.parent.parent
        target_node_item = e.control.parent.parent

        target_x = target_node_item.left + target_node.left + target_node.inout_point_diameter/2
        target_y = target_node_item.top + target_node.top + target_node.inout_point_diameter/2
        x = src_node_item.left + src_node.left + src_node.node_width - src_node.inout_point_diameter/2
        y = src_node_item.top + src_node.top + src_node.inout_point_diameter/2
        
        self.edge.add(target_node, src_node, e.control.content.key, src.content.key, x, y, target_x, target_y)
        
        if(self.callback_handler):
            m_node_event = NodeEvent(src_node, target_node, src.content.key, e.control.content.key)
            self.callback_handler(m_node_event)

        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    def drag_leave(self, e):
        e.control.content.border = None
        e.control.update()