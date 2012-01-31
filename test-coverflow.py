#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.menus.coverflow import Coverflow
from pyclut.effects.reflect import ReflectedItem
global current
current=1

def on_input(stage, event, coverflow, item_images):
	global current
	if event.keyval == keysyms.Left:
		coverflow.previous()
	elif event.keyval == keysyms.Right:
		coverflow.next()
	elif event.keyval == keysyms.a:
		coverflow.add(ReflectedItem(clutter.Texture(item_images[current])))
		current = (current + 1) % len(item_images)
	elif event.keyval == keysyms.s:
		coverflow.show()
	elif event.keyval == keysyms.h:
		coverflow.hide()
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Coverflow')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	x, y, width, height = (
		int(stage.get_width()/4),
		int(stage.get_height()-stage.get_height()/3),
		int(stage.get_width()/2),
		int(stage.get_height()-stage.get_height()/4),
	)

	coverflow = Coverflow(size=(1024, 512), item_size=(128,128), angle=70, inter_item_space=50, selection_depth=200)
	stage.add(coverflow)
	coverflow.hide()
	n_items = len(item_images)
	items = []
	stage.show()
	for image in item_images:
		coverflow.add(ReflectedItem(clutter.Texture(image)))
	coverflow.set_position(0, 400)
	coverflow.show()
	stage.connect('key-press-event', on_input, coverflow, item_images)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")



