#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.menus.thumbnail_menu import ThumbnailMenu
global current
current=1

def on_input(stage, event, thumbnailmenu, item_images):
	global current
	if event.keyval == keysyms.Left:
		thumbnailmenu.previous()
	elif event.keyval == keysyms.Right:
		thumbnailmenu.next()
	elif event.keyval == keysyms.Page_Down:
		thumbnailmenu.previous_page()
	elif event.keyval == keysyms.Page_Up:
		thumbnailmenu.next_page()
	elif event.keyval == keysyms.a:
		thumbnailmenu.add(clutter.Texture(item_images[current]))
		current = (current + 1) % len(item_images)
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Thumbnail Menu')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	thumbnailmenu = ThumbnailMenu(size=(1024, 512), item_size=(128,128), nb_item_by_page=4)
	stage.add(thumbnailmenu)
	n_items = len(item_images)
	items = []
	stage.show()
	for image in item_images:
		thumbnailmenu.add(clutter.Texture(image))
	thumbnailmenu.set_position(400, 200)
	stage.connect('key-press-event', on_input, thumbnailmenu, item_images)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")


