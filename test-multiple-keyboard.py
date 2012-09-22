#!/usr/bin/python

import clutter
from clutter import cogl

from test import PyClutTest
from pyclut.controls.keyboard import SimpleKeyboard, KeyboardLayout, PulseButtonFactory
from pyclut.basics.rectangle import RoundRectangle
from pyclut.effects.transitions import TransitionZone
from pyclut.effects.transitions.slide import SlideTransition
from pyclut.effects.transitions.rotate import RotateTransition
from pyclut.effects.transitions.zoom import ZoomTransition
from pyclut.effects.transitions.fade import FadeTransition


class MultipleKeyboardTest(PyClutTest):
	def __init__(self, transition_names=None, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)
		self._transition_names = transition_names or ["Rotate",]
		self._transitions = {
			"Slide" : (SlideTransition, {"zone_object" : self._stage,}),
			"Rotate" : (RotateTransition, {"direction" : clutter.RotateDirection.CCW, "axis" : clutter.AlignAxis.X_AXIS, "center" : (64, 64, -50), "style" : clutter.EASE_OUT_BOUNCE}),
#   		"Rotate" : (RotateTransition, {"direction" : clutter.RotateDirection.CW, "axis" : clutter.AlignAxis.Y_AXIS},),
			"Zoom" : (ZoomTransition, {},),
			"Fade" : (FadeTransition, {},),
		}
		self.current= "ABC"

	def _get_transition(self, transition_name, actor_in, actor_out):
		transition_class, transition_kwargs = self._transitions[transition_name]
		return transition_class(actor_in=actor_in, actor_out=actor_out, duration=500, **transition_kwargs)

	def createKeyboard(self, name, keymap):
		factory = PulseButtonFactory(background="./images/buttons/button.png")
		background = RoundRectangle()
		background.set_color("Black")
		return SimpleKeyboard(
			layout=KeyboardLayout(name, keymap),
			background=background,
			button_factory=factory,
			button_size=(48,48),
			inter_button_space=10
		)

	def key_pressed(self, event, key):
		if str(key) == "123":
			in_actor = self.keyboards["123"]
			out_actor = self.keyboards[self.current]
			transitions = [self._get_transition(transition_name, in_actor, out_actor) for transition_name in self._transition_names]
			[transition.start() for transition in transitions]
			self.current = "123"
		elif str(key) == "ABC":
			in_actor = self.keyboards["ABC"]
			out_actor = self.keyboards[self.current]
			transitions = [self._get_transition(transition_name, in_actor, out_actor) for transition_name in self._transition_names]
			[transition.start() for transition in transitions]
			self.current = "ABC"
		elif str(key) == "abc":
			in_actor = self.keyboards["abc"]
			out_actor = self.keyboards[self.current]
			transitions = [self._get_transition(transition_name, in_actor, out_actor) for transition_name in self._transition_names]
			[transition.start() for transition in transitions]
			self.current = "abc"

	def run(self):
		cogl.set_backface_culling_enabled(True)
		self.keyboards = {}
		key_map = [
			["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"],
			["N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
			["123", "abc"],
		]
		self.keyboards["ABC"] = self.createKeyboard("ABC", key_map)
		key_map = [
			["1", "2", "3",],
			["4", "5", "6",],
			["7", "8", "9",],
			["abc", "0", "ABC",],
		]
		self.keyboards["123"] = self.createKeyboard("123", key_map)
		key_map = [
			["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"],
			["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
			["123", "ABC"],
		]
		self.keyboards["abc"] = self.createKeyboard("abc", key_map)
		self._stage.add_actor(self.keyboards["ABC"])
		self._stage.add_actor(self.keyboards["123"])
		self._stage.add_actor(self.keyboards["abc"])
		self.keyboards["ABC"].set_position(
			self._stage.get_width()/2-self.keyboards["ABC"].get_width()/2,
			self._stage.get_height()/2-self.keyboards["ABC"].get_height()/2)
		self.keyboards["123"].set_position(
			self._stage.get_width()/2-self.keyboards["123"].get_width()/2,
			self._stage.get_height()/2-self.keyboards["123"].get_height()/2)
		self.keyboards["123"].hide()
		self.keyboards["abc"].set_position(
			self._stage.get_width()/2-self.keyboards["abc"].get_width()/2,
			self._stage.get_height()/2-self.keyboards["abc"].get_height()/2)
		self.keyboards["abc"].hide()
		[keyboard.connect("key-pressed", self.key_pressed) for keyboard in self.keyboards.values()]
		clutter.main()

if __name__ == '__main__':
	import sys
	test = MultipleKeyboardTest(sys.argv[1:], resolution=(800, 600), background_color="White")
	test.run()



