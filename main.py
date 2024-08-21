import flet as ft

from library.flet_node_editor import *
# Use of GestureDetector for with on_pan_update event for dragging card
# Absolute positioning of controls within stack
 
def main(page: ft.Page):

   def nodeA_callback_handler(e :NodeEvent):
      print(f"{e.src_item_id} {e.target_item_id}")
 
   edge = Edge()

   nodeA = Node(100, 200, 50, 10, edge)
   nodeB = Node(200, 400, 100, 300, edge)
   nodeC = Node(100, 250, 0, 0, edge)

   nodeA.append_output("volume", "tamashiro")
   nodeA.append_output("af", "top is good")
   nodeA.append_input("senchan", "sen suki")
   nodeB.append_input("val", "fa")
   nodeB.append_input("bb", "toshinori")
   nodeC.append_input("c_1", "network")
   nodeC.append_output("c_2", "anata")

   nodeA.register_callback(nodeA_callback_handler)

   page.theme = ft.theme.Theme(color_scheme_seed="green")
   page.add(ft.Stack(controls=[nodeA, nodeB, nodeC, edge], width=1000, height=500))
 
ft.app(target=main)