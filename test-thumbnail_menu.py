﻿#!/usr/bin/python

import clutter
from test import PyClutTest
from clutter import keysyms
from pyclut.menus.thumbnail_menu import ThumbnailMenu

class ThumbnailMenuTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def impl_on_input(self, stage, event):
		if event.keyval == keysyms.Left:
			self.thumbnailmenu.previous()
		elif event.keyval == keysyms.Right:
			self.thumbnailmenu.next()
		elif event.keyval == keysyms.Page_Down:
			self.thumbnailmenu.previous_page()
		elif event.keyval == keysyms.Page_Up:
			self.thumbnailmenu.next_page()
		elif event.keyval == keysyms.a:
			self.thumbnailmenu.add(clutter.Texture(self.get_image()))

	def run(self):
		nb_row = 4
		nb_column = 4
		item_size = 128
		inter_item = 10
		self.thumbnailmenu = ThumbnailMenu(
			size=(nb_column*(item_size+inter_item), nb_row*(item_size+inter_item)),
			item_size=(item_size, item_size),
			row=nb_row,
			column=nb_column,
			inter_item_space=inter_item,
		)
		self._stage.add(self.thumbnailmenu)
		self._stage.show()
		for rank in range(20):
			image = self.get_image()
			self.thumbnailmenu.add(clutter.Texture(image))
		self.thumbnailmenu.set_position(
			self._stage_center[0]-self.thumbnailmenu.get_size()[0]/2,
			self._stage_center[1]-self.thumbnailmenu.get_size()[1]/2
		)
		clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		test = ThumbnailMenuTest(image_directory=sys.argv[1])
	else:
		test = ThumbnailMenuTest()
	test.run()


