import math

import flet as ft
import flet.canvas as cv

class edge_constrain():
    def __init__(self, node_in, node_out, input_id, output_id, x, y, target_x, target_y):
        self.node_in = node_in
        self.node_out = node_out
        self.input_id = input_id
        self.output_id = output_id
        self.shapes_list_index = 0
        self.edge = cv.Path(
                [
                    cv.Path.MoveTo(x, y),
                    cv.Path.CubicTo( x + abs(target_x - x), y, target_x - x , target_y,target_x, target_y),
                ],
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
        
        self.shapes.append(
            new_edge_st.edge
        )
        new_edge_st.shapes_list_index = len(self.shapes) - 1
        self.edges.append(new_edge_st)
        self.update()

    def update_edge(self, node, item_id, x, y):
        for n in self.edges:
            if(n.node_in == node and n.input_id == item_id):
                n.edge.elements[1].x = x
                n.edge.elements[1].y = y
                n.edge.elements[1].cp1x = n.edge.elements[0].x + abs(x - n.edge.elements[0].x)/2
                n.edge.elements[1].cp1y = n.edge.elements[0].y
                n.edge.elements[1].cp2x = n.edge.elements[0].x + abs(x -  n.edge.elements[0].x)/2
                n.edge.elements[1].cp2y = y
                self.shapes.pop(n.shapes_list_index)
                self.shapes.insert(n.shapes_list_index, n.edge)
                self.update()
            elif(n.node_out == node and n.output_id == item_id):
                n.edge.elements[0].x = x
                n.edge.elements[0].y = y
                n.edge.elements[1].cp1x = x + abs(n.edge.elements[1].x - x)/2
                n.edge.elements[1].cp1y = y
                n.edge.elements[1].cp2x = x + abs(n.edge.elements[1].x - x)/2
                n.edge.elements[1].cp2y = n.edge.elements[1].y
                self.shapes.pop(n.shapes_list_index)
                self.shapes.insert(n.shapes_list_index, n.edge)
                self.update()

