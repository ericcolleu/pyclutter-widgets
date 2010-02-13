

import sys
import gobject
import clutter

from clutter import cogl

class Shape (clutter.Actor):
	__gtype_name__ = 'Shape'
	__gproperties__ = {
	  'color' : ( \
		str, 'color', 'Color', None, gobject.PARAM_READWRITE \
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
		self._is_pressed = False
		self.connect('button-press-event', self.do_button_press_event)
		self.connect('button-release-event', self.do_button_release_event)
		self.connect('leave-event', self.do_leave_event)

	def set_color (self, color):
		self._color = clutter.color_from_string(color)

	def do_set_property (self, pspec, value):
		if pspec.name == 'color':
			self._color = clutter.color_from_string(value)
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_get_property (self, pspec):
		if pspec.name == 'color':
			return self._color
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
	
	def __draw_shape(self, width, height, color):
		self.do_draw_shape(width, height)
		cogl.set_source_color(color)
		cogl.path_fill()

	def do_paint (self):
		(x1, y1, x2, y2) = self.get_allocation_box()

		paint_color = self._color

		real_alpha = self.get_paint_opacity() * paint_color.alpha / 255
		paint_color.alpha = real_alpha

		self.__draw_shape(x2 - x1, y2 - y1, paint_color)

	def do_pick (self, pick_color):
		if self.should_pick_paint() == False:
			return

		(x1, y1, x2, y2) = self.get_allocation_box()
		self.__paint_star(x2 - x1, y2 - y1, pick_color)

	def do_clicked (self):
		sys.stdout.write("Clicked!\n")




