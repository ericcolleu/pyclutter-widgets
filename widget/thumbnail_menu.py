import clutter
from widget.reflect import ReflectedItem
from widget.animation import MoveAnimation, RotateAnimation, ScaleAnimation, DepthAnimation
from widget.utils import clamp_angle


class ThumbnailItemAnimation(MoveAnimation, OpacityAnimation, DepthAnimation):
	def __init__(self, destination, opacity, depth, duration, style, timeline=None, alpha=None):
		MoveAnimation.__init__(self, destination, duration, style, timeline=timeline, alpha=alpha)
		OpacityAnimation.__init__(self, opacity, duration, style, timeline=self._timeline, alpha=self._alpha)
		DepthAnimation.__init__(self, depth, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = MoveAnimation.do_prepare_animation(self)
		behaviours.extend(OpacityAnimation.do_prepare_animation(self))
		behaviours.extend(DepthAnimation.do_prepare_animation(self))
		return behaviours

class ThumbnailMenu(clutter.Group):
	__gtype_name__ = 'ThumbnailMenu'
	def __init__(self, x=0, y=0, size=(512, 128), item_size=(128, 128), nb_item_by_page=4, selection_depth=200, *children):
		clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._width = size[0]
		self._height = size[1]
		self._item_size = item_size
		self._nb_item_by_page = nb_item_by_page
		self._selected = 0
		self._selection_depth = selection_depth
		self._children = []
		self._pages = [clutter.Group(),]
		self._current_page = self._pages[0]
		if children:
			self.add(*children)

	def add(self, *children):
		[child.set_size(*self._item_size) for child in children]
		[child.set_opacity(0) for child in children]
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

	def __get_items_in_current_page(self):
		page_num = int(self._selected / self._nb_item_by_page)
		return self._children[page_num*self._nb_item_by_page:min((page_num+1)*self._nb_item_by_page, len(self._children))]

	def __update_items_position(self):
		pass

	def next(self):
		self._selected = min(self._selected + 1,len(self._children)-1)# % len(self._children)
		self.__update_items_position()

	def previous(self):
		self._selected = max(self._selected - 1, 0)# % len(self._children)
		self.__update_items_position()





