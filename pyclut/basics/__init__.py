

import sys
from gi.repository import Clutter, Cogl, GObject

class Shape (Clutter.Actor):
	"""Base abstract class to create custom shapes.
	A shape can be filled with a color or a texture,
	and emit the 'clicked' signal when mouse button is released on it.
	"""
	__gtype_name__ = 'Shape'
	__gproperties__ = {
	  'color' : ( \
		str, 'color', 'Color', None, GObject.PARAM_READWRITE \
	  ),
	  'texture' : ( \
		str, 'texture', 'Texture', None, GObject.PARAM_READWRITE \
	  ),
	}
	__gsignals__ = {
		'clicked' : ( \
		  GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, () \
		),
	}

	def __init__ (self, texture=None, color=None):
		Clutter.Actor.__init__(self)
		self._color = Clutter.Color.from_string(color or 'White')
		print 50* "*", self._color
		self._texture = texture
		self._is_pressed = False
		self.connect('button-press-event', self.do_button_press_event)
		self.connect('button-release-event', self.do_button_release_event)
		self.connect('leave-event', self.do_leave_event)

	def set_color(self, color):
		"""Fill the shape with the color given in parameter.
		color may be a Clutter.Color object or a string representing
		the color name.
		"""
		if isinstance(color, Clutter.Color):
			self._color = color
		else:
			self._color = Clutter.Color.from_string(color)
		print 50* "+", self._color

	def set_texture(self, image):
		"""Fill the shape with a texture given in parameter.
		image may be a Clutter.Texture object or a string
		representing the texture file path.
		"""
		if isinstance(image, Clutter.Texture):
			self._texture = image
		else:
			self._texture = Clutter.Texture(image)

	def do_set_property (self, pspec, value):
		if pspec.name == 'color':
			self._color = self.set_color(value)
		elif pspec.name == 'texture':
			self._color = Clutter.Texture(value)
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_get_property (self, pspec):
		if pspec.name == 'color':
			return self._color
		elif pspec.name == 'texture':
			return self._texture
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_button_press_event (self, actor, event):
		if event.button == 1:
			self._is_pressed = True
			Clutter.grab_pointer(self)
			return True
		else:
			return False

	def do_button_release_event (self, actor, event):
		if event.button == 1 and self._is_pressed == True:
			self._is_pressed = False
			Clutter.ungrab_pointer()
			self.emit('clicked')
			return True
		else:
			return False

	def do_leave_event (self, actor, event):
		if self._is_pressed == True:
			self._is_pressed = False
			Clutter.ungrab_pointer()
			return True
		else:
			return False

	def do_draw_shape(self, width, height):
		pass

	def __draw_shape(self, width, height, color=None, texture=None):
		print 50*"-", color
		if texture:
			Cogl.set_source_texture(texture)
		else:
			Cogl.set_source_color(color)
		self.do_draw_shape(width, height)
		Cogl.path_fill()

	def do_paint (self):
		(x1, y1, x2, y2) = self.get_allocation_box()
		if self._texture:
			self.__draw_shape(x2 - x1, y2 - y1, texture = self._texture.get_cogl_texture())
		else:
			self._color.alpha = self.get_paint_opacity()
			self.__draw_shape(x2 - x1, y2 - y1, color = self._color)

	def do_pick (self, pick_color):
		if self.should_pick_paint() == False:
			return

		(x1, y1, x2, y2) = self.get_allocation_box()
		self.__draw_shape(x2 - x1, y2 - y1, pick_color)

	def do_clicked (self):
		print "Clicked!"

	def do_destroy(self):
		self.unparent()




