#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.menus.thumbnail_menu import ThumbnailPage

def on_input(stage, event, thumbnailpage):
	if event.keyval == keysyms.Left:
		thumbnailpage.select((thumbnailpage.get_selected()+1)%20)
	elif event.keyval == keysyms.Right:
		thumbnailpage.select((thumbnailpage.get_selected()-1)%20)
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Thumbnail Page')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	thumbnailpage = ThumbnailPage(size=(1024,768), max_row=4, max_column=5, inter_item_space=60)
	stage.add_actor(thumbnailpage)
	n_items = len(item_images)
	items = []
	stage.show()
	images=3*item_images
	for image in images[:20]:
		thumbnailpage.add_actor(clutter.Texture(image))
	
	thumbnailpage.select(0)
	stage.connect('key-press-event', on_input, thumbnailpage)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")



