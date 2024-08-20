import flet as ft

from library.flet_node_editor import *
# Use of GestureDetector for with on_pan_update event for dragging card
# Absolute positioning of controls within stack
 
def main(page: ft.Page):
 
   edge = Edge()

   nodeA = Node(100, 200, 50, 10, edge)
   nodeB = Node(200, 400, 100, 300, edge)

   nodeA.connect(nodeB)
   nodeB.connect(nodeA)

   nodeA.append_output("volume", "tamashiro")
   nodeB.append_input("val", "fa")

   page.theme = ft.theme.Theme(color_scheme_seed="green")
   page.add(ft.Stack(controls=[nodeA, nodeB, edge], width=1000, height=500))
 
ft.app(target=main)