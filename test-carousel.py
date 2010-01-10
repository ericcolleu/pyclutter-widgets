#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from widget.carrousel import Carrousel
global current
current=1

def on_input(stage, event, carrousel, item_images):
	global current
	if event.keyval == keysyms.Left:
		carrousel.previous()
	elif event.keyval == keysyms.Right:
		carrousel.next()
	elif event.keyval == keysyms.a:
		carrousel.add(clutter.Texture(item_images[current]))
		current = (current + 1) % len(item_images)
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Carrousel')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	x, y, width, height = (
		int(stage.get_width()/4), 
		int(stage.get_height()-stage.get_height()/3),
		int(stage.get_width()/2),
		int(stage.get_height()-stage.get_height()/4),
	)
	
	carrousel = Carrousel(width=512, height=512)
	stage.add(carrousel)
	n_items = len(item_images)
	items = []
	stage.show()
	for image in item_images:
		carrousel.add(clutter.Texture(image))
	carrousel.set_position(512, 200)
	stage.connect('key-press-event', on_input, carrousel, item_images)
	clutter.main()

if __name__ == '__main__':
	main("./images")


