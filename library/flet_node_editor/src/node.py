import flet as ft

import math

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
        

        self.style_brim = style.get("brim", ft.colors.with_opacity(0.0, ft.colors.WHITE))
        self.style_box = style.get("box", ft.colors.RED_50)
        self.style_interface_in = style.get("interface_in", ft.colors.BLUE_100)
        self.style_interface_out = style.get("interface_out", ft.colors.PURPLE_300)
        self.style_text = style.get("text", ft.colors.BLACK)
        self.style_text_font_size = style.get("text_font_size", 8)
        self.style_item_bgcolor = style.get("item_bgcolor", ft.colors.with_opacity(0.0, ft.colors.WHITE))
        self.style_item_edge = style.get("item_edge", ft.colors.with_opacity(0.0, ft.colors.WHITE))
        self.style_header_text = style.get("header_text", ft.colors.BLACK)
        self.style_header_bgcolor = style.get("header_bgcolor", ft.colors.BLUE_400)

        self.mouse_cursor = ft.MouseCursor.MOVE
        self.on_pan_update = self.drag
        self.drag_interval = 5
        self.top = top
        self.left = left
        self.content = ft.Container(
            width=self.node_width,
            height=self.node_height,
            border_radius=ft.border_radius.all(6),
            bgcolor=self.style_brim,
            content=ft.Stack(
                [
                    ft.Container(
                        key="info",
                        border_radius=ft.border_radius.all(6),
                        bgcolor=self.style_box,
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
        view = Item_Header(text, self)
        self.content.content.controls.append(view)

    def append_output(self, id, text=None):
        output_pointer_pos_x = self.next_obj_left + self.node_width - self.inout_point_diameter/2
        output_pointer_pos_y = self.next_obj_top + self.inout_point_diameter/2
        m_data_param = data_param(id, output_pointer_pos_x, output_pointer_pos_y)
    
        view = Item_Interface_IN(m_data_param, self.next_obj_left, self.next_obj_top, text, id, self)

        self.next_obj_top += self.obj_height
        
        self.content.content.controls.append(view)

        self.outputs.append(id)

    def append_input(self, id, text=None):
        output_pointer_pos_x = self.next_obj_left + self.inout_point_diameter/2
        output_pointer_pos_y = self.next_obj_top + self.inout_point_diameter/2
        m_data_param = data_param(id, output_pointer_pos_x, output_pointer_pos_y)

        dragtarget = ft.DragTarget(
                    group="color",
                    content=ft.Container(
                        key=id,
                        width=self.inout_point_diameter,
                        height=self.inout_point_diameter,
                        bgcolor=self.style_interface_in,
                        shape=ft.BoxShape.CIRCLE,
                    ),
                    on_will_accept=self.drag_will_accept,
                    on_accept=self.drag_accept,
                    on_leave=self.drag_leave,
                )

        view = ft.Stack(
            [
                ft.Container(
                    content=dragtarget,
                ),
                ft.Container(
                    margin=ft.margin.only(left=self.inout_point_diameter),
                    content=ft.Text(
                    value=text, 
                    color=self.style_text,
                    ),
                ),
            ],
            key="obj",
            data=m_data_param,
            left=self.next_obj_left,
            top=self.next_obj_top,
            expand=True,
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