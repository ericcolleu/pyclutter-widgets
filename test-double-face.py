#!/usr/bin/python

import clutter

from test import PyClutTest
from pyclut.basics.double_face import DoubleFaceTexture
from pyclut.effects.reflect import RotatingItem


class OdoTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		self.timeline = clutter.Timeline(duration=3000)
		self.timeline.set_loop(True)
		self.alpha = clutter.Alpha(self.timeline, clutter.AnimationMode.LINEAR)
		self.behaviour = clutter.BehaviourRotate(clutter.AlignAxis.Y_AXIS, 0.0, 360.0, self.alpha, clutter.RotateDirection.CW)
		item = DoubleFaceTexture(
			front=self.get_image(),
			back=self.get_image(),
		)
		self._stage.show()
		self._stage.add(item)
		item.set_position(
			self._stage.get_size()[0]/2-item.get_size()[0]/2,
			self._stage.get_size()[1]/2-item.get_size()[1]/2
		)
		self.behaviour.set_center(int(item.get_width()/2), 0, 0)
		self.behaviour.apply(item)
		self.timeline.start()
		clutter.main()

if __name__ == '__main__':
	test = OdoTest()
	test.run()



