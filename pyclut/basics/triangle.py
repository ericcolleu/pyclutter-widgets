import sys
import gobject
import clutter

from clutter import cogl
from pyclut.basics import Shape

class Triangle (Shape):
    __gtype_name__ = 'Triangle'
    def do_draw_shape(self, width, height):
        cogl.path_move_to(width / 2, 0)
        cogl.path_line_to(width, height)
        cogl.path_line_to(0, height)
        cogl.path_line_to(width / 2, 0)
        cogl.path_close()

gobject.type_register(Triangle)


