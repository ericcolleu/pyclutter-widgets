import clutter
import gobject
from widget.animation import Animator

class Button(clutter.Group):
	__gtype_name__ = 'Button'
	__gsignals__ = {
		'pressed' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () ),
		'released' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () ),
	}

	def __init__(self, released_background, pressed_background):
		clutter.Group.__init__(self)
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
			self.emit("pressed")

	def _on_released(self, background, event):
		if event.button == 1:
			self._show_released()
			self.emit("released")

