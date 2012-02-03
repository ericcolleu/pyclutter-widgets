#!/usr/bin/python

import clutter
from test import PyClutTest
from clutter import keysyms
from pyclut.controls.clock import FlapClock

class FlapClockTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		self.clock = FlapClock()
		self._stage.add(self.clock)
		self._stage.show()
		self.clock.set_position(
			self._stage_center[0]-self.clock.get_size()[0]/2,
			self._stage_center[1]-self.clock.get_size()[1]/2
		)
		clutter.main()

if __name__ == '__main__':
	test = FlapClockTest()
	test.run()



