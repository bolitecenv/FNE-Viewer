import flet as ft


class Item_Header(ft.Stack):
    def __init__(self, text, param):
        super().__init__()
        self.left = param.disp_obj_offset
        self.top = 0
        self.width = param.obj_width - 20
        self.controls = [
            ft.Container(
                bgcolor=param.style_header_bgcolor,
                width=param.obj_width - 20,
                height=20,
                border_radius=ft.border_radius.only(top_left=6, top_right=6),
            ),
            ft.Row(
                    [
                        ft.Text(
                            value=text,
                            color=param.style_header_text,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]

class Item_Interface_IN(ft.Stack):
    def __init__(self, data, left, top, text, id, param):
        super().__init__()
        self.key = "obj"
        self.data = data
        self.left = left
        self.top = top

        draggable = ft.Draggable(
                            group="color",
                            content=ft.Container(
                                key=id,
                                width=param.inout_point_diameter,
                                height=param.inout_point_diameter,
                                bgcolor=param.style_interface_out,
                                shape=ft.BoxShape.CIRCLE,
                            ),
                        )

        self.controls = [
                ft.Container(
                    bgcolor=param.style_item_bgcolor,
                    width=param.obj_width,
                ),
                ft.Container(
                    margin=ft.margin.only(left=param.inout_point_diameter),
                    content=ft.Text(
                    value=text, 
                    color=param.style_text,
                    ),
                ),
                ft.Container(
                    left= param.obj_width - param.inout_point_diameter,
                    content=draggable,
                ),
        ]


class Item_Interface_OUT(ft.Stack):
    def __init__(self, data, left, top, text, id, param):
        pass