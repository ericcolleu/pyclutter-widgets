

import sys
import gobject
import clutter

from clutter import cogl

class Shape (clutter.Actor):
	"""Base abstract class to create custom shapes.
	A shape can be filled with a color or a texture,
	and emit the 'clicked' signal when mouse button is released on it.
	"""
	__gtype_name__ = 'Shape'
	__gproperties__ = {
	  'color' : ( \
		str, 'color', 'Color', None, gobject.PARAM_READWRITE \
	  ),
	  'texture' : ( \
		str, 'texture', 'Texture', None, gobject.PARAM_READWRITE \
	  ),
	}
	__gsignals__ = {
		'clicked' : ( \
		  gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () \
		),
	}

	def __init__ (self):
		clutter.Actor.__init__(self)
		self._color = clutter.color_from_string('White')
		self._texture = None
		self._is_pressed = False
		self.connect('button-press-event', self.do_button_press_event)
		self.connect('button-release-event', self.do_button_release_event)
		self.connect('leave-event', self.do_leave_event)

	def set_color(self, color):
		"""Fill the shape with the color given in parameter.
		color may be a clutter.Color object or a string representing
		the color name.
		"""
		if isinstance(color, clutter.Color):
			self._color = color
		else:
			self._color = clutter.color_from_string(color)

	def set_texture(self, image):
		"""Fill the shape with a texture given in parameter.
		image may be a clutter.Texture object or a string
		representing the texture file path.
		"""
		if isinstance(image, clutter.Texture):
			self._texture = image
		else:
			self._texture = clutter.Texture(image)

	def do_set_property (self, pspec, value):
		if pspec.name == 'color':
			self._color = clutter.color_from_string(value)
		elif pspec.name == 'texture':
			self._color = clutter.Texture(value)
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
			clutter.grab_pointer(self)
			return True
		else:
			return False

	def do_button_release_event (self, actor, event):
		if event.button == 1 and self._is_pressed == True:
			self._is_pressed = False
			clutter.ungrab_pointer()
			self.emit('clicked')
			return True
		else:
			return False

	def do_leave_event (self, actor, event):
		if self._is_pressed == True:
			self._is_pressed = False
			clutter.ungrab_pointer()
			return True
		else:
			return False

	def do_draw_shape(self, width, height):
		pass

	def __draw_shape(self, width, height, color=None, texture=None):
		if texture:
			cogl.set_source_texture(texture)
		else:
			cogl.set_source_color(color)
		self.do_draw_shape(width, height)
		cogl.path_fill()

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




