#!/usr/bin/python

import clutter

from test import PyClutTest
from pyclut.effects.transitions import TransitionZone
from pyclut.effects.transitions.slide import SlideTransition
from pyclut.menus.carrousel import Carrousel
from pyclut.menus.coverflow import Coverflow
from pyclut.menus.thumbnail_menu import ThumbnailMenu


class TransitionTest(PyClutTest):
	transitions = {
		"Slide" : SlideTransition,
	}
	def __init__(self, transition_name, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)
		self._menu = 0
		self._transition_class = self.transitions[transition_name]

	def _on_item_clicked(self, item, event):
		out_menu = self._menus[self._menu]
		self._menu = (self._menu + 1)%len(self._menus)
		in_menu = self._menus[self._menu]
		transition = self._transition_class(actor_in=in_menu, actor_out=out_menu, zone_object=self._stage, duration=500)
		transition.start()

	def _create_item(self, image):
		item = clutter.Texture(image)
		item.set_reactive(True)
		item.connect("button-release-event", self._on_item_clicked)
		return item

	def run(self):
		carrousel = Carrousel(size=(512,512), item_size=(128,128))
		coverflow = Coverflow(size=(512, 512), item_size=(128,128), angle=70, inter_item_space=50, selection_depth=200)
		thumbnailmenu = ThumbnailMenu(size=(300, 300), item_size=(128,128))
		coverflow.hide()
		thumbnailmenu.hide()
		self._menus = [carrousel, coverflow, thumbnailmenu]
		self._stage.add(carrousel)
		self._stage.add(coverflow)
		self._stage.add(thumbnailmenu)
		self._stage.show()
		for rank in range(10):
			image = self.get_image()
			carrousel.add(self._create_item(image))
			coverflow.add(self._create_item(image))
			thumbnailmenu.add(self._create_item(image))
		carrousel.set_position(
			self._stage.get_size()[0]/2-carrousel.get_size()[0]/2,
			self._stage.get_size()[1]/2-carrousel.get_size()[1]/2
		)
		clutter.main()

if __name__ == '__main__':
	test = TransitionTest("Slide")
	test.run()


