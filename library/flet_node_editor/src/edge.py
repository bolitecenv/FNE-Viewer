import math

import flet as ft
import flet.canvas as cv

class Edge(cv.Canvas):
    def __init__(self):
        super().__init__()
        self.edges = []
    
    def did_mount(self):
        #self.add(10,20,400,200)
        pass
    
    def add(self, x, y, target_x, target_y):
        self.shapes.append(
            cv.Line(
                x, y, target_x, target_y,
                paint=ft.Paint(
                    stroke_width=2,
                    color=ft.colors.PINK,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
        )
        self.update()