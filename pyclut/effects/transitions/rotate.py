import clutter
from pyclut.effects.transitions import Transition, Direction
from pyclut.animation import RotateAnimation, OpacityAnimation

class RotateAndFadeAnimation(RotateAnimation, OpacityAnimation):
	def __init__(self, angle, axis, direction, opacity, duration, style, timeline=None, alpha=None):
		RotateAnimation.__init__(self, angle, axis, direction, duration, style, timeline=timeline, alpha=alpha)
		OpacityAnimation.__init__(self, opacity, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = RotateAnimation.do_prepare_animation(self)
		behaviours.extend(OpacityAnimation.do_prepare_animation(self))
		return behaviours

class RotateTransition(Transition):
	def __init__(self, actor_in, actor_out, direction=clutter.ROTATE_CW, axis=clutter.Y_AXIS, final_position=None, duration=500, style=clutter.LINEAR):
		Transition.__init__(self, actor_out, actor_in, actor_out, final_position=final_position or actor_in.get_position(), duration=duration, style=style)
		self._axis = axis
		self._direction = direction
		self._duration = duration
		self._style = style

	def __prepare_in_position(self):
		self._actor_in.set_position(*self._final_position)
		self._actor_in.set_rotation(self._axis, 180.0, 0.0, 0.0, 0.0)
		self._actor_in.set_opacity(0)

	def __prepare_out_position(self):
		self._actor_out.set_rotation(self._axis, 0.0, 0.0, 0.0, 0.0)
		self._actor_out.set_opacity(255)

	def preset_position(self):
		actor_out_width, actor_out_height = self._actor_out.get_size()
		self._final_position = self._final_position or (self._zone_center[0]-actor_out_width/2,self._zone_center[1]-actor_out_height/2)
		self.__prepare_in_position()
		self.__prepare_out_position()

	def create_animations(self):
		self._actor_in.show()
		anim_in = RotateAndFadeAnimation(0, self._axis, self._direction, 255, self._duration, self._style)
		anim_out = RotateAndFadeAnimation(-180, self._axis, self._direction, 0, self._duration, self._style)
		return anim_in, anim_out


