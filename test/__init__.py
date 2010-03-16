import clutter
import glob
import os.path
from clutter import keysyms

class PyClutTest(object):
	def __init__(self, resolution=(1024, 768), background_color=None, image_directory="./images"):
		self._stage = clutter.Stage()
		self._stage.set_size(*resolution)
		self._stage.connect('destroy', clutter.main_quit)
		self._stage.set_color(clutter.color_from_string(background_color or "Black"))
		self._stage.set_title(self.__class__.__name__)
		self._stage.show()
		self.item_images = glob.glob(os.path.join(image_directory, "*.png"))
		self.current_image = 0
		self._stage_center = (self._stage.get_size()[0]/2, self._stage.get_size()[1]/2)
		self._stage.connect('key-press-event', self.on_input)

	def impl_on_input(self, *args):
		pass

	def on_input(self, stage, event):
		if event.keyval == keysyms.q:
			clutter.main_quit()
		else:
			self.impl_on_input(stage, event)

	def get_image(self):
		self.current_image = (self.current_image + 1) % len(self.item_images)
		return self.item_images[self.current_image-1]



