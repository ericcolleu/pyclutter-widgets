import clutter
import gobject
from widget.utils import clamp_angle

class Animation(clutter.Behaviour):
	__gtype_name__ = 'Animation'
	__gsignals__ = {
		'completed' : ( \
		  gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () \
		),
	}

	def __init__(self, duration, style, timeline=None, alpha=None):
		clutter.Behaviour.__init__(self)
		self._timeline = timeline or clutter.Timeline(duration)
		self._timeline.connect("completed", self._on_done)
		self._alpha = alpha or clutter.Alpha(self._timeline, style)
		self._behaviours = []
		self._actor = None

	def do_prepare_animation(self):
		return []
	
	def _on_done(self, timeline):
		[behaviour.remove_all() for behaviour in self._behaviours]
		self.emit("completed")
		
	def prepare(self):
		self._behaviours = self.do_prepare_animation()

	def apply(self, actor):
		self._actor = actor
		self.prepare()
		[behaviour.apply(actor) for behaviour in self._behaviours]

	def start(self):
		self._timeline.rewind()
		self._timeline.start()

class MoveAnimation(Animation):
	def __init__(self, destination, duration, style, timeline=None, alpha=None):
		Animation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._destination = destination

	def do_prepare_animation(self):
		start_x, start_y = self._actor.get_position()
		path = clutter.Path("M %s %s L %s %s" % (start_x, start_y, self._destination[0], self._destination[1]))
		return [clutter.BehaviourPath(self._alpha, path),]
		
class RotateAnimation(Animation):
	def __init__(self, angle, axis, direction, duration, style, timeline=None, alpha=None):
		Animation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._angle = angle
		self._axis = axis
		self._direction = direction

	def do_prepare_animation(self):
		return [clutter.BehaviourRotate(
			self._axis, 
			clamp_angle(self._actor.get_rotation(self._axis)[0]), 
			clamp_angle(self._angle), 
			self._alpha, 
			self._direction),]

class MoveAndRotateAnimation(MoveAnimation, RotateAnimation):
	def __init__(self, destination, angle, axis, direction, duration, style, timeline=None, alpha=None):
		MoveAnimation.__init__(self, destination, duration, style, timeline=timeline, alpha=alpha)
		RotateAnimation.__init__(self, angle, axis, direction, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = [MoveAnimation.do_prepare_animation(self),]
		behaviours += [RotateAnimation.do_prepare_animation(self),]
		return behaviours
		
class ScaleAnimation(Animation):
	def __init__(self, scale_x, scale_y, duration, style, timeline=None, alpha=None):
		Animation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._scale_x = scale_x
		self._scale_y = scale_y

	def do_prepare_animation(self):
		(cur_scale_x, cur_scale_y) = self._actor.get_scale()
		return [clutter.BehaviourScale(
			cur_scale_x, 
			cur_scale_y, 
			self._scale_x, 
			self._scale_y, 
			self._alpha),]

class OpacityAnimation(Animation):
	def __init__(self, opacity, duration, style, timeline=None, alpha=None):
		Animation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._opacity = opacity

	def do_prepare_animation(self):
		return [clutter.BehaviourOpacity(
			opacity_start=self._actor.get_opacity(), 
			opacity_end=self._opacity, 
			alpha=self._alpha),]

class TurnAroundAnimation(Animation):
	def __init__(self, center, radius, angle, tilt, duration, style, timeline=None, alpha=None):
		Animation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._radius = radius
		self._center = center
		self._angle = angle
		self._tilt = tilt

	def do_prepare_animation(self):
		behaviour = clutter.BehaviourEllipse(
			self._alpha,
			self._center[0],
			self._center[1],
			self._radius*2,
			self._radius*2,
			360, self._angle)
		behaviour.set_tilt(*self._tilt)
		return [behaviour,]

class Animator(object):
	def __init__(self, default_duration_ms=500, default_style=clutter.LINEAR):
		self._default_duration = default_duration_ms
		self._default_style = default_style
		self._behaviours = {}

	def _animation_done(self, timeline):
		for behaviour in self._behaviours[timeline]:
			behaviour.remove_all()

	def createMoveAnimation(self, destination, duration_ms=None, style=None):
		return MoveAnimation(
			destination,
			duration_ms or self._default_duration,
			style or self._default_style,
		)

	def createRotateAnimation(self, angle, axis=clutter.Y_AXIS, direction=clutter.ROTATE_CW, duration_ms=None, style=None):
		return RotateAnimation(
			angle, 
			axis, 
			direction,
			duration_ms or self._default_duration,
			style or self._default_style,
		)
		
	def createScaleAnimation(self, scale_x, scale_y, duration_ms=None, style=None):
		return ScaleAnimation(
			scale_x, 
			scale_y, 
			duration_ms or self._default_duration,
			style or self._default_style,
		)

	def createOpacityAnimation(self, opacity, duration_ms=None, style=None, *actors):
		return OpacityAnimation(
			opacity, 
			duration_ms or self._default_duration,
			style or self._default_style,
		)

	def createMoveAndRotateAnimation(self, destination, angle, axis, direction, duration_ms=None, style=None):
		return MoveAndRotateAnimation(
			destination, 
			angle, 
			axis, 
			direction,
			duration_ms or self._default_duration,
			style or self._default_style,
		)
		
	def turn_around(self, actor, center, ellipse_width, ellipse_height, angle, tilt=None, direction=clutter.ROTATE_CW, timeline=None, alpha=None):
		timeline, alpha = self._get_timeline_and_alpha(timeline, alpha)
		behavior = clutter.BehaviourEllipse(
			alpha,
			center[0],
			center[1],
			ellipse_width,
			ellipse_height,
			360, clamp_angle(angle))
		if tilt:
			behavior.set_tilt(*tilt)
		behavior.apply(actor)
		self._memoize_behaviour(behavior, timeline)
		return (behavior, timeline)

		
