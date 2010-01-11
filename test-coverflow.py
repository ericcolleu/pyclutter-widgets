#!/usr/bin/python

import gobject
import clutter

from clutter import cogl
import glob
import os.path
from clutter import keysyms
from widget.coverflow import HorizontalFlowBrowser
from widget.reflect import ReflectedItem

class Coverflow(HorizontalFlowBrowser):

	ITEM_SIZE = (128, 128)
	CACHED_ITEMS = 8
	VISIBLE_ITEMS = 3


	def __init__(self):
		self.albums = {}
		self.filtered = []
		HorizontalFlowBrowser.__init__(self)
		self.connect('selection-activated', self.on_activate_item)
		self.connect('selection-changed', self.on_selection_changed)
		self.setup_label()
		self.focused = None
		self.setup_icons()

	def setup_icons(self):
		pass

	def setup_label(self):
		self.label = clutter.Text()
		self.label.set_color(clutter.color_from_string('WHITE'))
		self.label.set_use_markup(True)
		self.label.set_ellipsize(True)
		self.add(self.label)

	def get_items_number(self):
		return len(self.filtered)

	def get_item(self, index):
		album = ReflectedItem(clutter.Texture(self.filtered[index]))
		album.set_reactive(True)
		album.connect('button-press-event', lambda i, e: self.focus_item(i.get_parent()))
		return album

	def on_selection_changed(self, coverflow, index):
		self.label.set_text('%s' % os.path.basename(self.filtered[index]))
		self.label.set_position((self.get_width()-self.label.get_width())/2, (self.get_height()-20))
		self.label.raise_top()
		if self.focused:
			self.focused.pop()

	def on_activate_item(self, obj, item):
		pass

	def clean_item(self, item):
		for elem in item.get_children()[3:]:
			item.remove(elem)

	def add_image(self, image):
		self.filtered.append(image)

	def previous(self):
		self.selection = (self.selection - 1) % len(self.filtered)

	def next(self):
		self.selection = (self.selection + 1) % len(self.filtered)

def on_input(stage, event, coverflow):
	if event.keyval == keysyms.Left:
		coverflow.previous()
	elif event.keyval == keysyms.Right:
		coverflow.next()
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.color_from_string('Black'))
	stage.set_title('Carousel')

	x, y, width, height = stage.get_width() / 2, stage.get_height() / 2, 200, 200
	coverflow = Coverflow()
	#carrousel = clutter.Group()
	stage.add(coverflow)

	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	n_items = len(item_images)
	items = []
	coverflow.set_position(0, 768-300)
	coverflow.set_size(1024, 150)
	for image in item_images:
		coverflow.add_image(image)

	coverflow.reload()
	stage.connect('key-press-event', on_input, coverflow)
	stage.show()
	clutter.main()

if __name__ == '__main__':
	main("./images")


