import clutter


class Panel(clutter.Group):
	__gtype_name__ = 'Panel'

	def __init__(self, size, background, *children):
		clutter.Group.__init__(self)
		if type(background) is str:
			self._background = clutter.Rectangle()
			self._background.set_color(clutter.color_from_string(background))
		else:
			self._background = background
		self._background.set_size(*size)
		self.add(self._background)
		if children:
			self.add(*children)

	def get_background(self):
		return self._background


