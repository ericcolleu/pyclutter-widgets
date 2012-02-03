import sys
import gobject
import clutter

from clutter import cogl
from pyclut.basics import Shape

class RoundRectangle(Shape):
	"""Rectangle Shape with rounded corner.
	You can set the radius property to change the rounded radius
	of corners (default is 10).
	"""
	__gtype_name__ = 'RoundRectangle'
	__gproperties__ = {
	  'radius' : (gobject.TYPE_INT, 'Radius', 'Rectangle rounded corner radius',
                0, 1, 0, gobject.PARAM_READWRITE),
	}
	def __init__ (self):
		Shape.__init__(self)
		self._radius = 10

	def set_radius(self, radius):
		"""Change the radius of corners.
		radius must be an integer.
		"""
		self._radius = radius

	def do_set_property (self, pspec, value):
		if pspec.name == 'radius':
			self._radius = value
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_get_property (self, pspec):
		if pspec.name == 'radius':
			return self._radius
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_draw_shape(self, width, height):
		cogl.path_round_rectangle (0, 0, width, height, self._radius, 5)

		cogl.path_close()


gobject.type_register(RoundRectangle)



