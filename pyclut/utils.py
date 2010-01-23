import clutter

def clamp(x, min=0, max=1):
	if x>max: return max
	elif x<min: return min
	else: return x

def clamp_angle(x):
	if x<0: x+=360
	if x>360: x-=360
	return x

def get_timeline_and_alpha(timeline=None, fps=30, duration=200, alpha=None):
	if not timeline:
		timeline = clutter.Timeline(fps=fps, duration=duration)
	if not alpha:
		alpha = clutter.Alpha(timeline, clutter.sine_inc_func)
	return (timeline, alpha)

def animate_actor_to_point(actor, point, timeline=None, fps=30, duration=200, alpha=None):
	(timeline, alpha) = get_timeline_and_alpha(timeline, fps, duration, alpha)
	start_x, start_y = actor.get_position()
	end_x, end_y = point
	path = clutter.Path("M %s %s L %s %s" % (start_x, start_y, end_x, end_y))
	behavior = clutter.BehaviourPath(alpha, path)
	behavior.apply(actor)
	return (behavior, timeline)

def animate_actor_to_angle(actor, axis, angle, direction, center=None, timeline=None, fps=30, duration=200, alpha=None):
	(timeline, alpha) = get_timeline_and_alpha(timeline, fps, duration, alpha)
	behavior = clutter.BehaviourRotate(axis, clamp_angle(actor.get_rotation(axis)[0]), clamp_angle(angle), alpha, direction)
	if center:
		behavior.set_center(*center)
	behavior.apply(actor)
	return (behavior, timeline)

def animate_actor_to_scale(actor, scale_x, scale_y, timeline=None, fps=30, duration=200, alpha=None):
	(timeline, alpha) = get_timeline_and_alpha(timeline, fps, duration, alpha)
	(cur_scale_x,cur_scale_y) = actor.get_scale()
	behavior = clutter.BehaviourScale(cur_scale_x, cur_scale_y, scale_x, scale_y, alpha)
	behavior.apply(actor)
	return (behavior, timeline)

def animate_actor_to_opacity(actor, opacity, timeline=None, fps=30, duration=200, alpha=None):
	(timeline, alpha) = get_timeline_and_alpha(timeline, fps, duration, alpha)
	start_op = actor.get_opacity()
	behavior = clutter.BehaviourOpacity(start_op, opacity, alpha)
	behavior.apply(actor)
	return (behavior, timeline)


