import clutter
import gobject
from pyclut.utils import clamp_angle, AbstractMethodNotImplemented

class AbstractAnimation(clutter.Behaviour):
	__gtype_name__ = 'AbstractAnimation'
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
		raise AbstractMethodNotImplemented("Animation must implement a do_prepare_animation method")

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

class MoveAnimation(AbstractAnimation):
	def __init__(self, destination, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._destination = destination

	def do_prepare_animation(self):
		start_x, start_y = self._actor.get_position()
		path = clutter.Path("M %s %s L %s %s" % (start_x, start_y, self._destination[0], self._destination[1]))
		behaviours = [clutter.BehaviourPath(alpha=self._alpha, path=path),]
		return behaviours

class CenteredRotateAnimation(AbstractAnimation):
	def __init__(self, angle, axis, direction, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._angle = angle
		self._axis = axis
		self._direction = direction

	def do_prepare_animation(self):
		behaviour = clutter.BehaviourRotate(
			axis=self._axis,
			angle_start=clamp_angle(self._actor.get_rotation(self._axis)[0]),
			angle_end=clamp_angle(self._angle),
			alpha=self._alpha,
			direction=self._direction)
		if self._axis == clutter.Y_AXIS:
			behaviour.set_center(int(self._actor.get_width()/2), 0, 0)
		elif self._axis == clutter.X_AXIS:
			behaviour.set_center(0, int(self._actor.get_height()/2), 0)
		return [behaviour,]

class RotateAnimation(AbstractAnimation):
	def __init__(self, angle, axis, direction, duration, style, center=None, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._angle = angle
		self._axis = axis
		self._direction = direction
		self._center = center

	def do_prepare_animation(self):
		behaviour = clutter.BehaviourRotate(
			axis=self._axis,
			angle_start=clamp_angle(self._actor.get_rotation(self._axis)[0]),
			angle_end=clamp_angle(self._angle),
			alpha=self._alpha,
			direction=self._direction)
		if self._center:
			behaviour.set_center(*center)
		return [behaviour,]

class MoveAndFlipAnimation(MoveAnimation, CenteredRotateAnimation):
	def __init__(self, destination, angle, axis, direction, duration, style, timeline=None, alpha=None):
		MoveAnimation.__init__(self, destination, duration, style, timeline=timeline, alpha=alpha)
		CenteredRotateAnimation.__init__(self, angle, axis, direction, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = MoveAnimation.do_prepare_animation(self)
		behaviours.extend(CenteredRotateAnimation.do_prepare_animation(self))
		return behaviours

class ScaleAnimation(AbstractAnimation):
	def __init__(self, scale_x, scale_y, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._scale_x = scale_x
		self._scale_y = scale_y

	def do_prepare_animation(self):
		(cur_scale_x, cur_scale_y) = self._actor.get_scale()
		return [clutter.BehaviourScale(
			x_scale_start=cur_scale_x,
			y_scale_start=cur_scale_y,
			x_scale_end=self._scale_x,
			y_scale_end=self._scale_y,
			alpha=self._alpha),]

class OpacityAnimation(AbstractAnimation):
	def __init__(self, opacity, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._opacity = opacity

	def do_prepare_animation(self):
		return [clutter.BehaviourOpacity(
			opacity_start=self._actor.get_opacity(),
			opacity_end=self._opacity,
			alpha=self._alpha),]

class TurnAroundAnimation(AbstractAnimation):
	def __init__(self, center, radius, angle, tilt, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._radius = radius
		self._center = center
		self._angle = angle
		self._tilt = tilt

	def do_prepare_animation(self):
		behaviour = clutter.BehaviourEllipse(
			alpha=self._alpha,
			x=self._center[0],
			y=self._center[1],
			width=self._radius*2,
			height=self._radius*2,
			start=360,
			end=self._angle)
		behaviour.set_tilt(*self._tilt)
		return [behaviour,]

class DepthAnimation(AbstractAnimation):
	def __init__(self, depth, duration, style, timeline=None, alpha=None):
		AbstractAnimation.__init__(self, duration, style, timeline=timeline, alpha=alpha)
		self._depth = depth

	def do_prepare_animation(self):
		return [clutter.BehaviourDepth(
			alpha=self._alpha,
			depth_start=int(self._actor.get_depth()),
			depth_end=self._depth),]

class ScaleAndFadeAnimation(ScaleAnimation, OpacityAnimation):
	def __init__(self, scale, opacity, duration, style, timeline=None, alpha=None):
		ScaleAnimation.__init__(self, scale, scale, duration, style, timeline=timeline, alpha=alpha)
		OpacityAnimation.__init__(self, opacity, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = ScaleAnimation.do_prepare_animation(self)
		behaviours.extend(OpacityAnimation.do_prepare_animation(self))
		return behaviours

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

	def createMoveAndFlipAnimation(self, destination, angle, axis, direction, duration_ms=None, style=None):
		return MoveAndFlipAnimation(
			destination,
			angle,
			axis,
			direction,
			duration_ms or self._default_duration,
			style or self._default_style,
		)

	def createDepthAnimation(self, depth, duration_ms=None, style=None):
		return DepthAnimation(
			depth,
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


