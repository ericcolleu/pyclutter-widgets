import clutter

class Carrousel(clutter.Group):
	__gtype_name__ = 'Carrousel'
	def __init__(self, x=0, y=0, size=(512,512), item_size=(128,128), *children):
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
		if children:
			self.add(*children)

	def __update_step(self):
		if self._children:
			self._step = int(360 / len(self._children))
		else:
			self._step = 0

	def __update_item(self, item, angle):
		item.ellipse = clutter.BehaviourEllipse(
			self._alpha,
			self._x,
			self._y,
			self._width,
			self._height,
			angle, angle)
		item.ellipse.set_tilt(*self._tilt)
		item.ellipse.apply(item)
		if angle == 360:
			scale = clutter.BehaviourScale(1.0, 1.0, 1.0, 1.0, self._alpha)
		else:
			scale = clutter.BehaviourScale(1.0, 1.0, 0.6, 0.6, self._alpha)
		scale.apply(item)
		item.angle = angle
		self._timeline.start()

	def add(self, *children):
		[child.set_size(*self._item_size) for child in children]
		self.do_add(*children)
		clutter.Group.add(self, *children)

	def do_add(self, *children):
		for child in children:
			self._children.append(child)
		self.__update_step()
		for index, child in enumerate(self._children):
			self.__update_item(child, index*self._step)

	def remove(self, *children):
		clutter.Group.remove(self, *children)
		self.do_remove(*children)

	def do_remove(self, *children):
		for child in children:
			if child in self._children:
				self._children.remove(child)
		self.__update_step()
		for index, child in enumerate(self._children):
			self.__update_item(child, index*self._step)

	def set_tilt(self, angles):
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

	def turn_item_left(self, item):
		item.ellipse.set_direction(clutter.ROTATE_CCW)
		item.ellipse.set_angle_start(item.angle)
		item.angle = (item.angle - self._step) % 360
		item.ellipse.set_angle_end(item.angle)

	def next(self):
		if self.get_reactive():
			self.set_reactive(False)
			for child in self._children:
				self.turn_item_right(child)
			self._timeline.start()

	def previous(self):
		if self.get_reactive():
			self.set_reactive(False)
			for child in self._children:
				self.turn_item_left(child)
			self._timeline.start()



