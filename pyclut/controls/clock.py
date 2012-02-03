import clutter
import gobject
import random

from datetime import datetime
from pyclut.basics.rectangle import RoundRectangle
from pyclut.effects.transitions.rotate import FlapTransition

class Flap(clutter.Group):
	__gtype_name__ = 'Flap'
	def __init__(self, value, size, font, background_color="White", text_color="Black"):
		clutter.Group.__init__(self)
		if background_color:
			self.background = RoundRectangle()
			self.background.set_size(*size)
			self.background.set_color(clutter.color_from_string(background_color))
			self.add(self.background)
		self.text = clutter.Text(font)
		self.text.set_text("%d" % value)
		self.text.set_color(clutter.color_from_string(text_color))
		self.text.set_position(
			(size[0]/2)-(self.text.get_width()/2),
			(size[1]/2)-(self.text.get_height()/2)
		)
		self.add(self.text)

class FlapClock(clutter.Group):
	__gtype_name__ = 'FlapClock'

	def __init__(self, font="Arial 48px", flap_size=(50, 75)):
		clutter.Group.__init__(self)
		self._font = font
		self._flap_size = flap_size
		self._number_values = 6*[0,]
		self._inter_space = 10
		self._flaps = []
		self.__update_numbers()
		self.__create_flaps()
		gobject.timeout_add_seconds(1, self.on_tick)

	def __create_flap(self, rank, value):
		flap = Flap(value, self._flap_size, self._font)
		flap.set_position(rank*(self._flap_size[0]+self._inter_space), 0)
		return flap

	def __create_flaps(self):
		for rank, num in enumerate(self._number_values):
			flap = self.__create_flap(rank, num)
			self._flaps.append(flap)
			self.add(flap)

	def __update_numbers(self):
		now = datetime.now()
		old_numbers = self._number_values
		self._number_values = [now.hour/10, now.hour%10, now.minute/10, now.minute%10, now.second/10, now.second%10]
		return [new != old for new, old in zip(self._number_values, old_numbers)]

	def __update_number(self, rank, new_value):
		new_flap = self.__create_flap(rank, new_value)
		self.add(new_flap)
		old_flap = self._flaps[rank]
		self._flaps[rank] = new_flap
		transition = FlapTransition(
			actor_in=new_flap,
			actor_out=old_flap,
			duration=random.randint(200, 500),
		)
		transition.connect("completed", self._on_transition_done, rank, old_flap)
		return transition, rank, old_flap

	def _on_transition_done(self, event, rank, old_flap):
		self.remove(old_flap)

	def do_refresh_clock(self, as_changed):
		transitions = []
		for rank, (value, animate) in enumerate(zip(self._number_values, as_changed)):
			if animate:
				transitions.append(self.__update_number(rank, value))
		[transition.start() for transition, rank, old_flap in transitions]

	def on_tick(self):
		self.do_refresh_clock(self.__update_numbers())
		return True

