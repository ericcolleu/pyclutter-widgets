import clutter
from widget.reflect import ReflectedItem
from widget.animation import MoveAnimation, RotateAnimation, ScaleAnimation, DepthAnimation
from widget.utils import clamp_angle


class CoverflowItemAnimation(MoveAnimation, RotateAnimation, ScaleAnimation, DepthAnimation):
	def __init__(self, destination, angle, axis, direction, scale, depth, duration, style, timeline=None, alpha=None):
		MoveAnimation.__init__(self, destination, duration, style, timeline=timeline, alpha=alpha)
		RotateAnimation.__init__(self, angle, axis, direction, duration, style, timeline=self._timeline, alpha=self._alpha)
		ScaleAnimation.__init__(self, scale, scale, duration, style, timeline=self._timeline, alpha=self._alpha)
		DepthAnimation.__init__(self, depth, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = MoveAnimation.do_prepare_animation(self)
		if clamp_angle(self._actor.get_rotation(self._axis)[0]) != clamp_angle(self._angle):
			behaviours.extend(RotateAnimation.do_prepare_animation(self))
		behaviours.extend(ScaleAnimation.do_prepare_animation(self))
		behaviours.extend(DepthAnimation.do_prepare_animation(self))
		return behaviours

class Coverflow(clutter.Group):
	__gtype_name__ = 'Coverflow'
	def __init__(self, x=0, y=0, size=(512, 128), item_size=(128, 128), *children):
		clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._width = size[0]
		self._height = size[1]
		self._item_size = item_size
		self._selected = 0
		self._inter_item_space = 50
		self._angle = 70
		self._selection_depth = 200
		self._children = []
		if children:
			self.add(*children)

	def add(self, *children):
		[child.set_size(*self._item_size) for child in children]
		self.do_add(*children)
		clutter.Group.add(self, *children)
		
	def do_add(self, *children):
		for child in children:
			self._children.append(child)
		self.__update_items_position()

	def remove(self, *children):
		clutter.Group.remove(self, *children)
		self.do_remove(*children)
		
	def do_remove(self, *children):
		for child in children:
			if child in self._children:
				self._children.remove(child)
		self.__update_items_position()

	def __apply_animation(self, item, destination, angle, direction, depth):
		anim = CoverflowItemAnimation(
			destination=(destination, self._y), 
			angle=angle, 
			axis=clutter.Y_AXIS, 
			direction=direction, 
			scale=1.0, 
			depth=depth,
			duration=200,
			style=clutter.EASE_IN_OUT_SINE
		)
		anim.apply(item)
		return anim
		
	def __update_items_position(self, selected_rotation=clutter.ROTATE_CW):
		center_x = self._x + self._width/2
		anims=[]
		print self._selected
		for index, item in enumerate(self._children[:self._selected]):
			anims.append(self.__apply_animation(
				item=item,
				destination=(center_x - (self._item_size[0]/2) - (self._inter_item_space*((self._selected-index)+1))), 
				angle=self._angle, 
				direction=clutter.ROTATE_CW, 
				depth=0.0))
			
		anims.append(self.__apply_animation(
			item=self._children[self._selected],
			destination=(center_x - self._item_size[0]/2), 
			angle=0, 
			direction=selected_rotation, 
			depth=self._selection_depth))

		if self._selected < (len(self._children)-1):
			for index, item in enumerate(self._children[self._selected+1:]):
				anims.append(self.__apply_animation(
					item=item,
					destination=(center_x + (self._item_size[0]/2) + (self._inter_item_space*(index+1))), 
					angle=360-self._angle, 
					direction=clutter.ROTATE_CCW, 
					depth=0.0))
		[anim.start() for anim in anims]

	def next(self):
		self._selected = min(self._selected + 1,len(self._children)-1)# % len(self._children)
		self.__update_items_position(clutter.ROTATE_CW)
		
	def previous(self):
		self._selected = max(self._selected - 1, 0)# % len(self._children)
		self.__update_items_position(clutter.ROTATE_CCW)




