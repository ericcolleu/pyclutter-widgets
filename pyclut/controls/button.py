import clutter
import gobject
from pyclut.animation import Animator
from pyclut.animation import ScaleAndFadeAnimation

class ImageButton(clutter.Group):
	__gtype_name__ = 'ImageButton'
	__gsignals__ = {
		'pressed' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
		'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, released_background, pressed_background, value=None):
		clutter.Group.__init__(self)
		self._value = value
		self._pressed_background = pressed_background
		self._pressed_background.set_opacity(0)
		self._released_background = released_background
		self._released_background.set_opacity(255)
		self._anim_factory = Animator(default_duration_ms=10)
		self._show = self._anim_factory.createOpacityAnimation(255)
		self._hide = self._anim_factory.createOpacityAnimation(0)
		self.add(self._pressed_background)
		self.add(self._released_background)
		self._released_background.connect("button-press-event", self._on_pressed)
		self._released_background.connect("button-release-event", self._on_released)
		self._released_background.set_reactive(True)

	def _show_pressed(self):
		self._show.apply(self._pressed_background)
		self._hide.apply(self._released_background)
		self._show.start()
		self._hide.start()

	def _show_released(self):
		self._show.apply(self._released_background)
		self._hide.apply(self._pressed_background)
		self._show.start()
		self._hide.start()

	def _on_pressed(self, background, event):
		if event.button == 1:
			self._show_pressed()
			self.emit("pressed", self._value)

	def _on_released(self, background, event):
		if event.button == 1:
			self._show_released()
			self.emit("released", self._value)


class TextButton(ImageButton):
	__gtype_name__ = 'TextButton'
	def __init__(self, text, released_background, pressed_background, value=None):
		ImageButton.__init__(self, released_background, pressed_background, value)
		self.text = clutter.Text(text)
		self.add(self.text)

class PulseButton(clutter.Group):
	__gtype_name__ = 'PulseButton'
	__gsignals__ = {
		'pressed' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, background, text=None, value=None):
		clutter.Group.__init__(self)
		self._value = value
		self.text = None
		self._background = background
		self._anim_factory = Animator(default_duration_ms=10)
		self._press = ScaleAndFadeAnimation(1.5, 0, 50, clutter.LINEAR)
		self._press.connect("completed", self._restore)
		self.add(self._background)
		if text:
			self.text = clutter.Text(text)
			self.add(self.text)
		self._background.connect("button-press-event", self._on_pressed)
		self._background.set_reactive(True)

	def _restore(self, *args):
		self.set_scale(1.0, 1.0)
		self.set_opacity(255)

	def _on_pressed(self, background, event):
		if event.button == 1:
			self._press.apply(self)
			self._press.start()
			self.emit("pressed", self._value)


