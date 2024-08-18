import flet as ft

from .node import Node

class Node_editor(ft.Stack):
    def __init__(self, settings, width, height):
        super().__init__()
        self.width = 1000
        self.height = 500


    def did_mount(self):
        pass


    def create_node(self):
        pass