import clutter
from pyclut.animation import Animator

class Direction:
	LEFT = "left"
	RIGHT = "right"
	TOP = "top"
	BOTTOM = "bottom"

class TransitionZone(object):
	def __init__(self, x, y, width, height):
		self._x = x
		self._y = y
		self._width = width
		self._height = height

	def get_size(self):
		return self._width, self._height

	def get_position(self):
		return self._x, self._y

class Transition(object):
	def __init__(self, zone_object, actor_in, actor_out, final_position, duration=100, style=clutter.LINEAR):
		self._zone = zone_object
		self._zone_size = self._zone.get_size()
		self._zone_position = self._zone.get_position()
		self._zone_center = (self._zone_position[0]+self._zone_size[0]/2, self._zone_position[1]+self._zone_size[1]/2)
		self._actor_in = actor_in
		self._actor_out = actor_out
		self._final_position = final_position
		self._anim_factory = Animator()

	def preset_position(self):
		pass

	def create_animations(self):
		pass

	def start(self):
		self.preset_position()
		self._actor_in.show()
		anim_in, anim_out = self.create_animations()
		anim_in.apply(self._actor_in)
		anim_out.apply(self._actor_out)
		anim_out.connect("completed", self._on_anim_completed)
		anim_in.start()
		anim_out.start()

	def _on_anim_completed(self, event):
		self._actor_out.hide()

