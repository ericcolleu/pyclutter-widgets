import gobject
import clutter
from pyclut.animation import MoveAnimation

class ScrollArea(clutter.Group):
	def __init__(self, size, *children):
		clutter.Group.__init__(self)
		self._size = size
		self._scroll_pix = 5
		self.set_reactive(True)
		self.connect('scroll-event', self.do_scroll_event)
		self.set_clip(0, 0, size[0], size[1])
		if children:
			self.add(*children)

	def do_scroll_event(self, widget, event):
		self.scroll(event.direction)

	def scroll(self, direction):
		clip = list(self.get_clip())
		if direction == clutter.SCROLL_UP:
			clip[1] -= self._scroll_pix
			anim = MoveAnimation((self.get_x(), self.get_y()+self._scroll_pix), 100, clutter.LINEAR)
		elif direction == clutter.SCROLL_DOWN:
			clip[1] += self._scroll_pix
			anim = MoveAnimation((self.get_x(), self.get_y()-self._scroll_pix), 100, clutter.LINEAR)
		elif direction == clutter.SCROLL_LEFT:
			clip[0] -= self._scroll_pix
			anim = MoveAnimation((self.get_x()+self._scroll_pix, self.get_y()), 100, clutter.LINEAR)
		elif direction == clutter.SCROLL_RIGHT:
			clip[0] += self._scroll_pix
			anim = MoveAnimation((self.get_x()-self._scroll_pix, self.get_y()), 100, clutter.LINEAR)
		if (clip[0]+clip[2]) > self.get_width() or (clip[1]+clip[3]) > self.get_height():
			return
		if clip[0] < 0 or clip[1] < 0:
			return
		anim.apply(self)
		anim.connect("completed", self.on_anim_done)
		anim.start()
		self.set_clip(*clip)


