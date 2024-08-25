import flet as ft

from library.flet_node_editor import *
 
def main(page: ft.Page):

   def nodeA_callback_handler(e :NodeEvent):
      print(f"{e.src_item_id} {e.target_item_id}")
 
   ndcss = ndcss_parser("./library/flet_node_editor/style/basic.ndcss")

   edge = Edge()

   nodeA = Node(100, 200, 50, 10, edge, ndcss)
   nodeB = Node(200, 400, 100, 300, edge, ndcss)
   nodeC = Node(100, 250, 0, 0, edge, ndcss)

   nodeA.append_header("he world")

   nodeA.append_output("volume", "tamashiro")
   nodeA.append_output("af", "top is good")
   nodeA.append_input("senchan", "sen suki")
   nodeB.append_input("val", "fa")
   nodeB.append_input("bb", "toshinori")
   nodeC.append_input("c_1", "network")
   nodeC.append_output("c_2", "anata")

   nodeA.register_callback(nodeA_callback_handler)

   #page.theme = ft.theme.Theme(color_scheme_seed="green")
   page.add(ft.Stack(controls=[nodeA, nodeB, nodeC, edge], width=1000, height=500))
 
ft.app(target=main)