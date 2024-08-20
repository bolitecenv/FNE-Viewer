import math

import flet as ft
import flet.canvas as cv

class edge_constrain():
    def __init__(self, node_in, node_out, input_id, output_id, x, y, target_x, target_y):
        self.node_in = node_in
        self.node_out = node_out
        self.input_id = input_id
        self.output_id = output_id
        self.edge = cv.Line(
                x, y, target_x, target_y,
                paint=ft.Paint(
                    stroke_width=2,
                    color=ft.colors.PINK,
                    style=ft.PaintingStyle.STROKE,
                ),
            )

class Edge(cv.Canvas):
    def __init__(self):
        super().__init__()
        self.edges = []
    
    def did_mount(self):
        pass
    
    def add(self, node_in, node_out, node_in_item_id, node_out_item_id, x, y, target_x, target_y):
        new_edge_st = edge_constrain(
            node_in,
            node_out,
            node_in_item_id,
            node_out_item_id,
            x, y ,target_x, target_y,
        )
        print(vars(new_edge_st))
        self.shapes.append(
            new_edge_st.edge
        )
        self.update()