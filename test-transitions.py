#!/usr/bin/python

import clutter
from clutter import cogl

from test import PyClutTest
from pyclut.effects.transitions import TransitionZone
from pyclut.effects.transitions.slide import SlideTransition
from pyclut.effects.transitions.rotate import RotateTransition, FlapTransition
from pyclut.effects.transitions.zoom import ZoomTransition
from pyclut.effects.transitions.fade import FadeTransition
from pyclut.menus.carrousel import Carrousel
from pyclut.menus.coverflow import Coverflow
from pyclut.menus.thumbnail_menu import ThumbnailMenu


class TransitionTest(PyClutTest):
	def __init__(self, transition_names, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)
		self._menu = 0
		self._transition_names = transition_names
		self._transitions = {
			"Slide" : (SlideTransition, {"zone_object" : self._stage,}),
			"Rotate" : (RotateTransition, {"direction" : clutter.RotateDirection.CCW, "axis" : clutter.AlignAxis.X_AXIS, "center" : (64, 64, -50), "style" : clutter.EASE_OUT_BOUNCE}),
			"Flap" : (FlapTransition, {},),
			"Zoom" : (ZoomTransition, {},),
			"Fade" : (FadeTransition, {},),
		}

	def _get_transition(self, transition_name, actor_in, actor_out):
		transition_class, transition_kwargs = self._transitions[transition_name]
		return transition_class(actor_in=actor_in, actor_out=actor_out, duration=500, **transition_kwargs)

	def _on_item_clicked(self, item, event):
		out_menu = self.objects[self.current]
		self.current = (self.current + 1)%len(self.objects)
		in_menu = self.objects[self.current]
		transitions = [self._get_transition(transition_name, in_menu, out_menu) for transition_name in self._transition_names]
		[transition.start() for transition in transitions]

	def _create_item(self, image):
		item = clutter.Texture(image)
		item.set_reactive(True)
		item.connect("button-release-event", self._on_item_clicked)
		return item

	def run(self):
		cogl.set_backface_culling_enabled(True)
		self.objects = [self._create_item(self.get_image()) for rank in range(10)]
		self.current = 0
		self._stage.show()
		for obj in self.objects:
			obj.set_position(
				self._stage.get_size()[0]/2-obj.get_size()[0]/2,
				self._stage.get_size()[1]/2-obj.get_size()[1]/2
			)
			obj.hide()
			self._stage.add(obj)
		self.objects[0].show()
		clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		test = TransitionTest(sys.argv[1:])
	else:
		test = TransitionTest(["Slide",])
	test.run()


