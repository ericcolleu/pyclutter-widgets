#!/usr/bin/python

import clutter
from test import PyClutTest
from clutter import keysyms
from pyclut.controls.scrollable import ScrollArea

class ScrollTextTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def impl_on_input(self, stage, event):
		if event.keyval == keysyms.Left:
			self.area.scroll(clutter.SCROLL_LEFT)
		elif event.keyval == keysyms.Right:
			self.area.scroll(clutter.SCROLL_RIGHT)
		elif event.keyval == keysyms.Up:
			self.area.scroll(clutter.SCROLL_UP)
		elif event.keyval == keysyms.Down:
			self.area.scroll(clutter.SCROLL_DOWN)

	def run(self):
		txt = """12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890
12345678901234567890"""
		self.text = clutter.Text()
		self.text.set_text(txt)
		self.text.set_color(clutter.Color(255, 255, 255, 255))

		self.area = ScrollArea((100, 100), self.text)
		self._stage.add(self.area)
		self._stage.show()
		self.area.set_position(
			self._stage_center[0]-self.area.get_size()[0]/2,
			self._stage_center[1]-self.area.get_size()[1]/2
		)
		clutter.main()

if __name__ == '__main__':
	test = ScrollTextTest()
	test.run()



