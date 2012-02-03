import clutter
from pyclut.utils import clamp_angle

# TODO: Add a "select_item" or "select" method
class Carrousel(clutter.Group):
	"""Carrousel menu is a list of items turning around an ellipse."""
	__gtype_name__ = 'Carrousel'
	def __init__(self, x=0, y=0, size=(512,512), item_size=(128,128), fade_ratio=0, *children):
		"""Constructor
		Carrousel(x, y, size, item_size, *children) -> Carrousel instance
		x, y : carrousel position (default is x=0, y=0)
		size : witdh and height of the carrousel (default is (512, 512))
		item_size : width and height of a menu item (default is (128, 128))
		children : optional list of item to add to the menu.
		"""
		clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._width = size[0]
		self._height = size[1]
		self._item_size = item_size
		self._children = []
		self._step = 0
		self._tilt = (300.0, 360.0, 360.0)
		self._timeline = clutter.Timeline(duration=100)
		self._timeline.connect('completed', self.anim_completed)
		self._alpha = clutter.Alpha(self._timeline, clutter.LINEAR)
		self._selected_scale = 1.2
		self._unselected_scale = 1.0
		self._selected_depth = 100
		self._unselected_depth = 0
		self._fade_ratio = fade_ratio
		if children:
			self.add(*children)

	def __update_step(self):
		if self._children:
			self._step = int(360 / len(self._children))
		else:
			self._step = 0

	def __set_item_opacity(self, item):
		if item.rank < (len(self._children) / 2):
			item.opacity = clutter.BehaviourOpacity(
				opacity_start=item.get_opacity(),
				opacity_end=max(10, 255-item.rank*self._fade_ratio),
				alpha=self._alpha
			)
		else:
			item.opacity = clutter.BehaviourOpacity(
				opacity_start=item.get_opacity(),
				opacity_end=max(10, 255-(len(self._children) - item.rank)*self._fade_ratio),
				alpha=self._alpha
			)
		item.opacity.apply(item)

	def __update_opacity(self, item):
		if not hasattr(item, "opacity"):
			self.__set_item_opacity(item)
			return
		if item.rank < (len(self._children) / 2):
			item.opacity.set_bounds(
				opacity_start=item.get_opacity(),
				opacity_end=max(10, 255-item.rank*self._fade_ratio)
			)
		else:
			item.opacity.set_bounds(
				opacity_start=item.get_opacity(),
				opacity_end=max(10, 255-(len(self._children) - item.rank)*self._fade_ratio)
			)

	def __update_item(self, item, angle, rank):
		angle = clamp_angle(90+self._step*rank)
		item.ellipse = clutter.BehaviourEllipse(
			self._alpha,
			self._x,
			self._y,
			self._width,
			self._height,
			angle, angle)
		item.ellipse.set_tilt(*self._tilt)
		item.ellipse.apply(item)
		item.rank = rank
		if rank == 0:
			item.scale = clutter.BehaviourScale(1.0, 1.0, self._selected_scale, self._selected_scale, self._alpha)
			item.depth = clutter.BehaviourDepth(item.get_depth(), self._selected_depth, self._alpha)
		else:
			item.scale = clutter.BehaviourScale(1.0, 1.0, self._unselected_scale, self._unselected_scale, self._alpha)
			item.depth = clutter.BehaviourDepth(item.get_depth(), self._unselected_depth, alpha=self._alpha)
		item.scale.apply(item)
		item.depth.apply(item)
		item.angle = angle
		self.__update_opacity(item)
		self._timeline.start()

	def add(self, *children):
		"""Add a list of items to the carrousel menu.
		carrousel.add(item1, item2, item3) -> return None
		"""
		[child.set_size(*self._item_size) for child in children]
		self.do_add(*children)
		clutter.Group.add(self, *children)

	def do_add(self, *children):
		for child in children:
			self._children.append(child)
		self.__update_step()
		for index, child in enumerate(self._children):
			self.__update_item(child, index*self._step, index)

	def remove(self, *children):
		clutter.Group.remove(self, *children)
		self.do_remove(*children)

	def do_remove(self, *children):
		for child in children:
			if child in self._children:
				self._children.remove(child)
		self.__update_step()
		for index, child in enumerate(self._children):
			self.__update_item(child, index*self._step, index)

	def set_tilt(self, angles):
		"""Set the view angle in the 3 axis.
		carrousel.set_tilt((300.0, 360.0, 360.0)) -> return None
		"""
		self._tilt = angles
		for item in self._children:
			item.set_tilt(*self._tilt)

	def anim_completed(self, timeline):
		self.set_reactive(True)

	def turn_item_right(self, item):
		item.ellipse.set_direction(clutter.ROTATE_CW)
		item.ellipse.set_angle_start(item.angle)
		item.angle = (item.angle + self._step) % 360
		item.ellipse.set_angle_end(item.angle)
		item.rank = (item.rank + 1) % len(self._children)
		x_start, y_start, x_end, y_end = item.scale.get_bounds()
		depth_start, depth_end = item.depth.get_bounds()
		if item.rank == 0:
			item.scale.set_bounds(x_end, y_end, self._selected_scale, self._selected_scale)
			item.depth.set_bounds(depth_end, self._selected_depth)
		else:
			item.scale.set_bounds(x_end, y_end, self._unselected_scale, self._unselected_scale)
			item.depth.set_bounds(depth_end, self._unselected_depth)
		self.__update_opacity(item)

	def turn_item_left(self, item):
		item.ellipse.set_direction(clutter.ROTATE_CCW)
		item.ellipse.set_angle_start(item.angle)
		item.angle = (item.angle - self._step) % 360
		item.ellipse.set_angle_end(item.angle)
		item.rank = (item.rank - 1) % len(self._children)
		x_start, y_start, x_end, y_end = item.scale.get_bounds()
		depth_start, depth_end = item.depth.get_bounds()
		if item.rank == 0:
			item.scale.set_bounds(x_end, y_end, self._selected_scale, self._selected_scale)
			item.depth.set_bounds(depth_end, self._selected_depth)
		else:
			item.scale.set_bounds(x_end, y_end, self._unselected_scale, self._unselected_scale)
			item.depth.set_bounds(depth_end, self._unselected_depth)
		self.__update_opacity(item)

	def next(self):
		"""Select the next item.
		carrousel.next() -> return None
		"""
		if self.get_reactive():
			self.set_reactive(False)
			for child in self._children:
				self.turn_item_right(child)
			self._timeline.start()

	def previous(self):
		"""Select the previous item.
		carrousel.next() -> return None
		"""
		if self.get_reactive():
			self.set_reactive(False)
			for child in self._children:
				self.turn_item_left(child)
			self._timeline.start()


