import sys
import gobject
import clutter

from clutter import cogl
from pyclut.basics import Shape

class SixBranchStar (Shape):
	__gtype_name__ = 'SixBranchStar'
	
	def do_draw_shape(self, width, height):
		cogl.path_move_to(0, height/4)
		cogl.path_line_to(width, height/4)
		cogl.path_line_to(width/2, height)
		cogl.path_line_to(0, height/4)

		cogl.path_move_to(0, height*3/4)
		cogl.path_line_to(width, height*3/4)
		cogl.path_line_to(width/2, 0)
		cogl.path_line_to(0, height*3/4)

		cogl.path_close()


gobject.type_register(SixBranchStar)


