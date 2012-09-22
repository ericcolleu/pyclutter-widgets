#!/usr/bin/python

import clutter

from test import PyClutTest
from pyclut.controls.keyboard import SimpleKeyboard, KeyboardLayout, PulseButtonFactory
from pyclut.basics.rectangle import RoundRectangle


class SimpleKeyboardTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		key_map = [
			["A", "B", "C", "D"],
			["N", "O", "P", "Q", "R", "S"],
			["N", "O", "P"],
			["1", "2", "3", "4", "5"],
		]
		factory = PulseButtonFactory(background="./images/buttons/button.png")
		background = RoundRectangle()
		background.set_color("Black")
		keyboard = SimpleKeyboard(
			layout=KeyboardLayout("layout", key_map),
			background=background,
			button_factory=factory,
			button_size=(48,48),
			inter_button_space=10
		)
		self._stage.add_actor(keyboard)
		keyboard.set_position(
			self._stage.get_width()/2-keyboard.get_width()/2,
			self._stage.get_height()/2-keyboard.get_height()/2)
		clutter.main()

if __name__ == '__main__':
	test = SimpleKeyboardTest(resolution=(800, 600), background_color="White")
	test.run()


