#!/usr/bin/python

import clutter
from test import PyClutTest
from clutter import keysyms
from pyclut.controls.scrollable import ScrollArea, Scrollbar
from pyclut.controls.text import TextContainer

class ScrollTextTest(PyClutTest):
	def __init__(self, *args, **kwargs):
		PyClutTest.__init__(self, *args, **kwargs)

	def run(self):
		txt = 100*(4*"12345678901234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"+"\n")
		label = TextContainer(txt)
		label.set_line_wrap(False)

		area = ScrollArea(label)
		area.set_size(600,400)
		area.set_position(100,40)
		v_scrollbar = Scrollbar()
		v_scrollbar.set_size(40,400)
		v_scrollbar.set_position(50,40)
		h_scrollbar = Scrollbar(horizontal=True)
		h_scrollbar.set_size(600,40)
		h_scrollbar.set_position(100,450)
		self._stage.add_actor(v_scrollbar)
		self._stage.add_actor(h_scrollbar)
		self._stage.add_actor(area)
		v_scrollbar.connect('scroll_position',area.callback_position)
		h_scrollbar.connect('scroll_position',area.callback_position)

		self.text = clutter.Text()
		self.text.set_text(txt)
		self.text.set_color(clutter.Color(255, 255, 255, 255))
		print "start test"
		clutter.main()

if __name__ == '__main__':
	test = ScrollTextTest()
	test.run()



