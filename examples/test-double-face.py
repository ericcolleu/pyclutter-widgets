#!/usr/bin/python

from gi.repository import Clutter
from pyclut.basics.double_face import DoubleFaceTexture
from pyclut.effects.reflect import RotatingItem
from pyclut.test_tools import PyClutTest



class OdoTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		self.timeline = Clutter.Timeline.new(3000)
		self.timeline.set_loop(True)
		self.alpha = Clutter.Alpha.new_full(self.timeline, Clutter.AnimationMode.LINEAR)
		self.behaviour = Clutter.BehaviourRotate.new(
			self.alpha,
			Clutter.AlignAxis.Y_AXIS,
			Clutter.RotateDirection.CW,
			0.0,
			360.0,
		)
		item = DoubleFaceTexture(
			front=self.get_image(),
			back=self.get_image(),
		)
		self._stage.show()
		self._stage.add_actor(item)
		item.set_position(
			self._stage.get_size()[0]/2-item.get_size()[0]/2,
			self._stage.get_size()[1]/2-item.get_size()[1]/2
		)
		self.behaviour.set_center(int(item.get_width()/2), 0, 0)
		self.behaviour.apply(item)
		self.timeline.start()
		Clutter.main()

if __name__ == '__main__':
	test = OdoTest()
	test.run()



