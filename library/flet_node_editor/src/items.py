import flet as ft


class Item_Header(ft.Stack):
    def __init__(self, param, text="", style={}):
        super().__init__()
        self.left = param.disp_obj_offset
        self.top = 0
        self.width = param.obj_width
        self.controls = [
            ft.Container(
                bgcolor=style.get("bgcolor", None),
                width=param.obj_width,
                height=20,
                border_radius=ft.border_radius.only(top_left=6, top_right=6),
            ),
            ft.Row(
                    [
                        ft.Text(
                            value=text,
                            size=style.get("text_size", None),
                            color=style.get("text_color", None),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]

class Item_Interface_IN(ft.Stack):
    def __init__(
                    self,
                    id,
                    param,
                    data=None,
                    left=0,
                    top=0,
                    text="",
                    style={},
                ):
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
                                bgcolor=style.get("inout_point_color", None),
                                shape=ft.BoxShape.CIRCLE,
                            ),
                        )

        self.controls = [
                ft.Container(
                    width=param.node_width,
                    height=param.obj_height,
                ),
                ft.Row(
                    #margin=ft.margin.only(left=param.inout_point_diameter),
                    left=param.disp_obj_offset,
                    controls=[
                        ft.Container(
                            bgcolor=style.get("bgcolor", None),
                            alignment=ft.alignment.center_right,
                            padding=ft.padding.only(right=param.disp_obj_offset),
                            width=param.obj_width,
                            content=ft.Text(
                                value=text,
                                size=style.get("text_size", None),
                                color=style.get("text_color", None),
                            )
                        ),
                    ]
                ),
                ft.Container(
                    left= param.node_width - param.inout_point_diameter,
                    content=draggable,
                ),
        ]


class Item_Interface_OUT(ft.Stack):
    def __init__(
                    self,
                    id,
                    param,
                    data=None,
                    left=0,
                    top=0,
                    text="",
                    style={},
                ):
        super().__init__()

        self.key = "obj"
        self.data = data
        self.left = left
        self.top = top

        dragtarget = ft.DragTarget(
                    group="color",
                    content=ft.Container(
                        key=id,
                        width=param.inout_point_diameter,
                        height=param.inout_point_diameter,
                        bgcolor=style.get("inout_point_color", None),
                        shape=ft.BoxShape.CIRCLE,
                    ),
                    on_will_accept=param.drag_will_accept,
                    on_accept=param.drag_accept,
                    on_leave=param.drag_leave,
                )

        self.controls = [
                ft.Container(
                        content=dragtarget,
                ),
                ft.Container(
                    margin=ft.margin.only(left=param.inout_point_diameter),
                    content=ft.Text(
                    value=text, 
                    size=style.get("text_size", None),
                    color=style.get("text_color", None),
                    ),
                ),
        ]