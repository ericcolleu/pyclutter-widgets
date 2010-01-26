import clutter
from pyclut.animation import DepthAnimation
from pyclut.utils import clamp_angle


class PageFullError(Exception):
	pass

class ThumbnailPage(clutter.Group):
	__gtype_name__ = 'ThumbnailPage'
	def __init__(self, size=(512, 512), max_row=2, max_column=2, selection_depth=75, item_size=(128, 128), inter_item_space=10):
		clutter.Group.__init__(self)
		self._max_item = max_row * max_column
		self._max_row = max_row
		self._max_column = max_column
		self._selection_depth = selection_depth
		self._selected = -1
		self._item_size = item_size
		self._width = size[0]
		self._height = size[1]
		self._inter_item_space = inter_item_space
		self._children=[]

	def add(self, *children):
		if self.is_full():
			raise PageFullError()
		[child.set_size(*self._item_size) for child in children]
		self._children+=children
		clutter.Group.add(self, *children)
		self.__update()

	def __update(self):
		i=0
		delta_y = (self._item_size[1] + self._inter_item_space)
		delta_x = (self._item_size[0] + self._inter_item_space)
		y = self._height - (self._max_row * delta_y)
		try:
			for r in range(self._max_row):
				x = self._width - (self._max_column * delta_x)
				for c in range(self._max_column):
					self._children[i].set_position(x, y)
					i+=1
					x+=delta_x
				y+=delta_y
		except IndexError:
			pass
		self.select(self._selected)
			
	def _select_item(self, selected):
		self._selected = selected
		if selected >=0:
			anim = DepthAnimation(self._selection_depth, duration=200, style=clutter.LINEAR)
			anim.apply(self._children[selected])
			anim.start()
		
	def _unselect_items(self, selected):
		anims=[]
		for i,item in enumerate(self._children):
			if i != selected:
				anim = DepthAnimation(0, duration=200, style=clutter.LINEAR)
				anim.apply(item)
				anims.append(anim)
		[anim.start() for anim in anims]
		
	def select(self, index_):
		self._select_item(index_)
		self._unselect_items(index_)
		
	def is_empty(self):
		return (len(self._children) == 0)
		
	def is_full(self):
		return (len(self._children) >= self._max_item)

	def get_selected(self):
		return self._selected
		
class ThumbnailMenu(clutter.Group):
	__gtype_name__ = 'ThumbnailMenu'
	def __init__(self, x=0, y=0, size=(512, 128), item_size=(128, 128), row=2, column=2, selection_depth=200, *children):
		clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._selected = 0
		self._args = size, row, column, selection_depth, item_size
		self._item_by_page = row * column
		self._current_page = ThumbnailPage(*self._args)
		self._pages.append(self._current_page)
		clutter.Group.add(self, self._current_page)
		self._nb_children=0
		if children:
			self.add(*children)

	def add(self, *children):
		for child in children:
			try:
				self._nb_children+=1
				self._current_page.add(child)
			except PageFullError:
				self._current_page = ThumbnailPage(*self._args)
				self._pages.append(self._current_page)
				clutter.Group.add(self, self._current_page)
				self._current_page.add(child)
		self.__update()

	def remove(self, *children):
		clutter.Group.remove(self, *children)
		self.do_remove(*children)

	def do_remove(self, *children):
		for child in children:
			self._nb_children-=1
		self.__update()

	def __get_items_in_current_page(self):
		page_num = int(self._selected / self._nb_item_by_page)
		return self._children[page_num*self._nb_item_by_page:min((page_num+1)*self._nb_item_by_page, len(self._children))]

	def __update(self):
		for i,page in enumerate(self._pages):
			if page != self._current_page:
				page.hide()
			else:
				current_page_index = i
		self._current_page.select(self._selected-((current_page_index-1)*self._item_by_page))

	def next(self):
		self._selected = min(self._selected + 1,len(self._children)-1)# % len(self._children)
		self.__update()

	def previous(self):
		self._selected = max(self._selected - 1, 0)# % len(self._children)
		self.__update()

	def next_page(self):
		pass
	
	def previous_page(self):
		pass




