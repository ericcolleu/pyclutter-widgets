#!/usr/bin/python

from gi.repository import Clutter
from pyclut.test_tools import PyClutTest
from pyclut.menus.thumbnail_menu import ThumbnailMenu
from pyclut.controls.button import PulseButton

class ThumbnailMenuTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def impl_on_input(self, stage, event):
		if get_keyval(event) == Clutter.Left:
			self.thumbnailmenu.previous()
		elif get_keyval(event) == Clutter.Right:
			self.thumbnailmenu.next()
		elif get_keyval(event) == Clutter.Page_Down:
			self.thumbnailmenu.previous_page()
		elif get_keyval(event) == Clutter.Page_Up:
			self.thumbnailmenu.next_page()
		elif get_keyval(event) == Clutter.a:
			self.thumbnailmenu.add_actor(Clutter.Texture.new_from_file(self.get_image()))

	def run(self):
		nb_row = 4
		nb_column = 4
		item_size = 128
		inter_item = 10
		self.thumbnailmenu = ThumbnailMenu(
			#size=(nb_column*(item_size+inter_item), nb_row*(item_size+inter_item)),
			item_size=(item_size, item_size),
			row=nb_row,
			column=nb_column,
			inter_item_space=inter_item,
			selection_depth=50
		)
		self._stage.add_actor(self.thumbnailmenu)
		self._stage.show()
		for rank in range(20):
			image = self.get_image()
			item = PulseButton(Clutter.Texture.new_from_file(image))
			self.thumbnailmenu.add_actor(item)
		self.thumbnailmenu.set_position(
			self._stage_center[0]-self.thumbnailmenu.get_size()[0]/2,
			self._stage_center[1]-self.thumbnailmenu.get_size()[1]/2
		)
		Clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		test = ThumbnailMenuTest(image_directory=sys.argv[1])
	else:
		test = ThumbnailMenuTest()
	test.run()


