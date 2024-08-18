import flet as ft

import math

from .edge import Edge

class Node(ft.GestureDetector):
    def __init__(self, width, height, top, left, edge):
        super().__init__()
        self.main_content = ft.Ref[ft.Column()]
        self.edge = edge

        self.target_node = None
        self.inputs = []
        self.outputs = []

        self.mouse_cursor = ft.MouseCursor.MOVE
        self.on_pan_update = self.drag
        self.drag_interval = 5
        self.top = top
        self.left = left
        self.content = ft.Container(
            width=width,
            height=height,
            border_radius=ft.border_radius.all(6),
            bgcolor=ft.colors.AMBER_100,
            content=ft.Column(
                [ft.Text("hello")],
                ref=self.main_content,
                ),
        )

    def drag(self, e: ft.DragUpdateEvent):
       e.control.top = max(0, e.control.top + e.delta_y)
       e.control.left = max(0, e.control.left + e.delta_x)
       e.control.update()
       self.re_draw_connection()

    def re_draw_connection(self):
        if(self.target_node is None):
            return
        
        draw_len_x = self.left - self.target_node.left
        draw_len_y = self.top - self.target_node.top
        draw_len = math.sqrt(draw_len_x**2 + draw_len_y**2)
        print(draw_len)

    def connect(self, target_node):
        self.target_node = target_node
        draw_len_x = self.left - self.target_node.left
        draw_len_y = self.top - self.target_node.top
        draw_len = math.sqrt(draw_len_x**2 + draw_len_y**2)
        print(draw_len)

    def append_output(self, id, text=None):

        view = ft.Row(
            [
                ft.Text(
                    value=text, 
                    color=ft.colors.BLACK,
                    ),
                ft.Draggable(
                            group="color",
                            content=ft.Container(
                                key=id,
                                width=10,
                                height=10,
                                bgcolor=ft.colors.BLACK,
                                shape=ft.BoxShape.CIRCLE,
                            ),
                        ),
            ]
        )
        
        self.content.content.controls.append(view)

        self.outputs.append(id)

    def append_input(self, id, text=None):

        view = ft.Row(
            [
                ft.Text(
                    value=text, 
                    color=ft.colors.BLACK,
                    ),
                ft.DragTarget(
                    group="color",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border_radius=5,
                    ),
                    on_will_accept=self.drag_will_accept,
                    on_accept=self.drag_accept,
                    on_leave=self.drag_leave,
                ),
            ]
        )
        
        self.content.content.controls.append(view)
        
        self.inputs.append(id)


    def drag_will_accept(self, e):
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
        )
        
        e.control.update()

    def drag_accept(self, e: ft.DragTargetAcceptEvent):
        src = self.page.get_control(e.src_id)
        print(src.content.key)
        x = self.left
        y = self.top
        target_x = self.target_node.left
        target_y = self.target_node.top
        print(e.control.parent.parent.controls[1].controls)
        self.edge.add(x, y, target_x, target_y)
        print(f"{x} {y} {target_x} {target_y}")
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    def drag_leave(self, e):
        e.control.content.border = None
        e.control.update()