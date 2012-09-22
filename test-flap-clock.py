#!/usr/bin/python

import clutter
from test import PyClutTest
from clutter import keysyms
from pyclut.controls.clock import FlapClock, HalfFlap

class FlapClockTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		self.clock = FlapClock()
		self._stage.add_actor(self.clock)
		self._stage.show()
		self.clock.set_position(
			self._stage_center[0]-self.clock.get_size()[0]/2,
			self._stage_center[1]-self.clock.get_size()[1]/2
		)
		flap = HalfFlap(2, (50, 50), True, "Arial 48px")
		self.timeline = clutter.Timeline(duration=3000)
		self.timeline.set_loop(True)
		self.alpha = clutter.Alpha(self.timeline, clutter.AnimationMode.LINEAR)
		self.behaviour = clutter.BehaviourRotate(clutter.AlignAxis.Y_AXIS, 0.0, 360.0, self.alpha, clutter.RotateDirection.CW)
		flap.set_position(
			self._stage_center[0]-self.clock.get_size()[0]/2,
			self._stage_center[1]-self.clock.get_size()[1]/2 + 100
		)
		self._stage.add_actor(flap)
		self.behaviour.set_center(int(flap.get_width()/2), 0, 0)
		self.behaviour.apply(flap)
		self.timeline.start()
		clutter.main()

if __name__ == '__main__':
	test = FlapClockTest()
	test.run()



