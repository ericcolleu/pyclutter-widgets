#!/usr/bin/python

from gi.repository import Clutter

import glob, time
import os.path
from pyclut.menus.thumbnail_menu import ThumbnailPage

def on_input(stage, event, thumbnailpage):
	if event.keyval == Clutter.Left:
		thumbnailpage.select((thumbnailpage.get_selected()+1)%20)
	elif event.keyval == Clutter.Right:
		thumbnailpage.select((thumbnailpage.get_selected()-1)%20)
	elif event.keyval == Clutter.q:
		Clutter.main_quit()

def do_quit(*args):
	Clutter.main_quit()

def main(image_directory):
	Clutter.init(sys.argv)
	stage = Clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', do_quit)
	stage.set_color(Clutter.Color.new(0, 0, 0, 255))
	stage.set_title('Thumbnail Page')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	thumbnailpage = ThumbnailPage(size=(1024,768), max_row=4, max_column=5, inter_item_space=60)
	stage.add_actor(thumbnailpage)
	n_items = len(item_images)
	items = []
	stage.show()
	images=3*item_images
	for image in images[:20]:
		thumbnailpage.add_actor(Clutter.Texture.new_from_file(image))

	thumbnailpage.select(0)
	stage.connect('key-press-event', on_input, thumbnailpage)
	Clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")



