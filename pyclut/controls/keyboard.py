import clutter
import gobject
from pyclut.controls.button import TextButton, PulseButton
from pyclut.basics.rectangle import RoundRectangle

class Key(object):
	def __init__(self, value=None, text=None):
		self.value = value
		self.text = text

	def __str__(self):
		if self.text:
			return self.text
		return ""

	def __call__(self, *args, **kwargs):
		if self.value:
			return value
		return self.text

class Modifier(Key):
	def __init__ (self, pass_to_layout, value=None, text=None):
		SpecialKey.__init__(self, value, text)
		self.pass_to_layout = pass_to_layout

class KeyFactory(object):
	def getKey(self, key):
		if isinstance(key, str):
			return Key(text=key)
		elif isinstance(key, Key):
			return key
		elif isinstance(key, list) or isinstance(key, tuple):
			return Key(text=key[0], value=key[1])

class KeyboardLayout:
	def __init__ (self, name, key_map=None):
		self.name = name
		self._key_map = []
		self.__key_factory = KeyFactory()
		if key_map:
			self.set_key_map(key_map)

	def set_key_map(self, key_map):
		self._key_map = [[self.__key_factory.getKey(key) for key in line] for line in key_map]

	def get_key_map(self):
		return self._key_map

class PulseButtonFactory(object):
	def __init__(self, background=None, color=None):
		self._background = background
		self._color = color

	def get_button(self, text=None, value=None):
		if self._background:
			background=clutter.Texture(self._background)
		else:
			background=clutter.RoundRectangle()
			background.set_color(self._color or "White")
		return PulseButton(background, text=text, value=value)

class SimpleKeyboard(clutter.Group):
	__gtype_name__ = 'SimpleKeyboard'
	__gsignals__ = {
		'key-pressed' : ( gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, layout=None, background=None, button_factory=None,
		button_size=(75,75), inter_button_space=0):
		clutter.Group.__init__(self)
		self._layout = layout
		self._button_size = button_size
		self._inter_button_space = inter_button_space
		self._background = background or RoundRectangle()
		self._button_factory = button_factory or PulseButtonFactory()
		self.add(self._background)
		self.__create_buttons()

	def __create_buttons(self):
		line_width = 0
		lines = self._layout.get_key_map()
		height = self._inter_button_space + len(lines) * (self._button_size[1]+self._inter_button_space)
		y=self._inter_button_space
		for line in lines:
			nb_key = len(line)
			line_width = max(line_width, self._inter_button_space + nb_key*(self._button_size[0]+self._inter_button_space))
			x=self._inter_button_space
			for key in line:
				button=self._button_factory.get_button(text=str(key), value=key)
				button.set_size(*self._button_size)
				self.add(button)
				button.set_position(x, y)
				x += self._button_size[0]+self._inter_button_space
			y += self._button_size[1]+self._inter_button_space
		self._background.set_size(line_width, height)

	def _on_button_released(self, event, key):
		self.emit("key-pressed", key())


