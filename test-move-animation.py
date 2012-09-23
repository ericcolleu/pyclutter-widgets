#!/usr/bin/python

from gi.repository import Clutter
from test import PyClutTest
from pyclut.animation import MoveAnimation

class MoveAnimationTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def on_button_press(self, stage, event):
		anim = MoveAnimation((event.x, event.y), 500, Clutter.AnimationMode.LINEAR)
		anim.connect("completed", self._on_done)
		anim.apply(self.item)
		anim.start()

	def _on_done(self, event):
		print "done"

	def run(self):
		self._stage.connect('key-press-event', self.on_input)
		self.item = Clutter.Texture.new_from_file(self.get_image())
		self._stage.add_actor(self.item)
		self._stage.show()
		self._stage.connect('button-press-event', self.on_button_press)
		Clutter.main()

if __name__ == '__main__':
	test = MoveAnimationTest()
	test.run()



