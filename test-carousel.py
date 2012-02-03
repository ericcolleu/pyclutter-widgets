#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.menus.carrousel import Carrousel
from pyclut.effects.reflect import ReflectedItem
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
	stage.set_size(1024,768)
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

	carrousel = Carrousel(size=(512,512), item_size=(128,128), fade_ratio=50)
	stage.add(carrousel)
	n_items = len(item_images)
	items = []
	stage.show()
	for rank, image in enumerate(item_images):
		text = clutter.Text("Courrier New 24 px")
		text.set_text("%d" % rank)
		text.set_color(clutter.color_from_string("White"))
		item = clutter.Group()
		item.add(ReflectedItem(clutter.Texture(image)))
		item.add(text)
		carrousel.add(item)
	carrousel.set_position(
		stage.get_size()[0]/2-carrousel.get_size()[0]/2,
		stage.get_size()[1]/2-carrousel.get_size()[1]/2
	)
	stage.connect('key-press-event', on_input, carrousel, item_images)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")

