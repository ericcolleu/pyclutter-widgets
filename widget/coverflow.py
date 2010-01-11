import clutter
import gobject

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

class FlowBrowser(clutter.Group):
	"""A base class for items picker views like coverflow, override get_items_number and get_item to use it"""

	__gsignals__ = {
		'selection-changed' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,) ),
		'selection-activated' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_OBJECT,) ),
		'reloaded' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () ),
	}

	CACHED_ITEMS = 12
	ANIM_DURATION_MS = 200

	def __init__(self):
		clutter.Group.__init__(self)
		self._setup_events()
		self._setup_timeline_and_alpha()
		self.items = []
		self.reload()

	def reload(self):
		self.remove_all_items()
		self.items = []
		self.behaviors = []
		self._selection = 0
		self._fill_cache()
		self.place_items()
		self.emit('reloaded')
		self.emit('selection-changed', self.selection)

	def remove_all_items(self):
		for item in self._cached_items():
			self.remove(item)

	def _cached_items(self):
		"""Returns the items in cache"""
		return filter(None, self.items)

	def _setup_events(self):
		self.set_reactive(True)
		self.connect('scroll-event', self.on_scroll)

	def _setup_timeline_and_alpha(self):
		self.timeline = clutter.Timeline(self.ANIM_DURATION_MS)
		self.timeline.connect('completed', self.anim_completed)

		self.alpha = clutter.Alpha(self.timeline, clutter.EASE_IN_SINE)

	def _set_selection(self, selection):
		"""Change the current selection and reflect change in the view"""
		if self._selection != selection:
			if self._selection<selection:
				move_forward = True
			else:
				move_forward = False
			self._selection = selection
			self._fill_cache()
			self.place_items(move_forward)
			self.emit('selection-changed', selection)

	def _get_selection(self):
		return self._selection

	selection = property(_get_selection, _set_selection)

	def get_items_number(self):
		raise NotImplementedError

	def get_item(self, index):
		raise NotImplementedError

	def add_item(self, item, index=None):
		"""Add an item to the view"""
		if index is None: index=len(self.items)
		self.items.insert(index,item)
		self.add(item)
		self.place_new_item(item, index)

	def place_new_item(self, item, index):
		pass

	def insert_item(self, item, index=None):
		"""Insert an item and show it immediatly"""
		if index:
			if len(self.items)>index and index <= self.selection:
				self._selection += 1
		self.add_item(item, index)
		self.place_items()

	def anim_completed(self, tl):
		self._reduce_cache()

	def place_item(self, item, move_forward=False):
		"""Place the item in the view and animate the changes"""
		index = self.items.index(item)
		delta = index - self.selection

		self.anim_behaviors.extend(self.get_behaviors(item, delta, move_forward, self.alpha))

		self.timeline.rewind()
		self.timeline.start()

		if self.items[index-1]:
			if delta>0: item.lower_actor(self.items[index-1])
			else: item.raise_actor(self.items[index-1])

	def place_items(self, move_forward=False):
		"""Replace all items in the view according to the current selection index"""
		self.anim_behaviors = []
		for item in self._cached_items():
			self.place_item(item, move_forward)

	def get_behaviors(self, item, delta, move_forward, alpha):
		"""Returns animations behaviors, basic implementation meant to be overriden
		"""
		point = ((self.size[0]-item.get_size()[0])/2+item.get_width()*delta, (self.size[1]-item.get_size()[1])/2)
		(p_behavior, tl) = animate_actor_to_point(item, point, timeline=self.timeline, alpha=self.alpha)
		return [p_behavior]

	def _fill_cache(self):
		"""Fill the cache according to the ITEMS_CACHED value
		"""
		start_index = max(self.selection-self.CACHED_ITEMS, 0)
		end_index = min(self.selection+self.CACHED_ITEMS, self.get_items_number())
		total_size = self.get_items_number()
		while(total_size>len(self.items)):
			self.items.append(None)
		for i in range(start_index, end_index):
			if not self.items[i]:
				del self.items[i]
				self.add_item(self.get_item(i), i)

	def _reduce_cache(self):
		"""Reduce the cache and remove unused items from the view"""
		for i in self._cached_items():
			index = self.items.index(i)
			if abs(self.selection-index)>self.CACHED_ITEMS:
				self.remove(i)
				self.items[index] = None
				del i

	def on_scroll(self, fb, event):
		if event.direction == clutter.SCROLL_DOWN and self.selection>0:
			self.selection-=1
		elif event.direction == clutter.SCROLL_UP and self.selection<len(self.items)-1:
			self.selection+=1
		return True

	def focus_item(self, item, event=None):
		if self.items.index(item) == self.selection:
			self.emit('selection-activated',item)
		self.selection = self.items.index(item)

class HorizontalFlowBrowser(FlowBrowser):
	"""A coverflow like flowbrowser"""

	COVER_DIST=20
	FRONT_SIZE=100
	MAX_ANGLE = 70
	MIN_SCALE = 1
	MAX_SCALE=1.7
	VISIBLE_ITEMS = 12
	FADING_ITEMS = 3
	ITEM_SIZE = (100, 100)

	def __init__(self):
		FlowBrowser.__init__(self)
		self.VISIBLE_ITEMS = self.CACHED_ITEMS

	def refresh_params(self):
		self.MAX_SCALE = self.get_height()*(1.5)/(self.ITEM_SIZE[1]*2.0)
		self.MIN_SCALE = self.get_height()/(self.ITEM_SIZE[1]*2.0)
		self.COVER_DIST = (self.get_width()/2-self.FRONT_SIZE-20)/self.VISIBLE_ITEMS

	def set_size(self, width, height):
		FlowBrowser.set_size(self, width, height)
		self.refresh_params()
		self.place_items()

	def calc_angle(self, delta, move_forward):
		if delta == 0:
			if move_forward:
				rotation_dir = clutter.ROTATE_CW
			else:
				rotation_dir = clutter.ROTATE_CCW
			angle = 0

		if delta>0:
			rotation_dir = clutter.ROTATE_CCW
			angle = 360 - self.MAX_ANGLE

		if delta<0:
			rotation_dir = clutter.ROTATE_CW
			angle = self.MAX_ANGLE

		return (angle, rotation_dir)

	def calc_pos(self, delta):
		if (delta == 0):
			return 0
		dist = ((abs(delta)-1) * self.COVER_DIST) + self.FRONT_SIZE
		if delta > 0: return dist
		else: return -dist

	def calc_scale(self, delta):
		if delta == 0: return self.MAX_SCALE
		else: return self.MIN_SCALE

	def calc_opacity(self, delta):
		delta = abs(delta)
		if delta < self.VISIBLE_ITEMS-self.FADING_ITEMS:
			return 255
		else:
			delta -= self.VISIBLE_ITEMS-self.FADING_ITEMS
			return clamp(255*(self.FADING_ITEMS - delta)/self.FADING_ITEMS, 0, 255)

	def place_new_item(self, item, index):
		delta = index - self.selection
		if delta>0:
			item.set_position(self.get_width()+int(item.get_width()*self.MIN_SCALE), (self.get_height()-int(item.get_height()*self.MIN_SCALE))/2)
		else:
			item.set_position(-int(item.get_width()*self.MIN_SCALE*2), (self.get_height()-int(item.get_height()*self.MIN_SCALE))/2)
		item.set_scale(self.MIN_SCALE, self.MIN_SCALE)
		item.set_opacity(0)

	def get_behaviors(self, item, delta, move_forward, alpha):
		size = item.get_size()
		behaviors = []

		if delta==0:
			point = ((self.get_size()[0]-item.get_size()[0]*self.MAX_SCALE)/2+self.calc_pos(delta), (self.get_size()[1]-item.get_size()[1]*self.MAX_SCALE)/2)
		else:
			point = ((self.get_size()[0]-item.get_size()[0]*self.MIN_SCALE)/2+self.calc_pos(delta), (self.get_size()[1]-item.get_size()[1]*self.MIN_SCALE)/2)
		(p_behavior, tl) = animate_actor_to_point(item, point, timeline=self.timeline, alpha=self.alpha)
		behaviors.append(p_behavior)

		scale = self.calc_scale(delta)
		(s_behavior, tl) = animate_actor_to_scale(item, scale, scale, timeline=self.timeline, alpha=self.alpha)
		behaviors.append(s_behavior)

		angle_start = item.get_rotation(clutter.Y_AXIS)[0]
		angle_start = clamp_angle(angle_start)
		(angle_end, direction) = self.calc_angle(delta, move_forward)
		if abs(angle_start-angle_end)>1 and abs(angle_start-angle_end)<359:
			(r_behavior, tl) = animate_actor_to_angle(item, clutter.Y_AXIS, angle_end, direction, (size[0]/2, 0, 0), timeline = self.timeline, alpha=self.alpha)
			behaviors.append(r_behavior)

		(o_behavior, tl) = animate_actor_to_opacity(item, self.calc_opacity(delta), timeline=self.timeline, alpha=self.alpha)
		behaviors.append(o_behavior)

		return behaviors


