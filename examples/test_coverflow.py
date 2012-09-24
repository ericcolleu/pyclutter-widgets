#!/usr/bin/python

from gi.repository import Clutter
from pyclut.menus.coverflow import Coverflow
import glob
import sys
import os.path

global current
current=1

def on_input(stage, event, coverflow, item_images):
	global current
	if event.keyval == Clutter.KEY_Left:
		coverflow.previous()
	elif event.keyval == Clutter.KEY_Right:
		coverflow.next()
	elif event.keyval == Clutter.a or event.keyval == Clutter.A:
		coverflow.add_actor(Clutter.Texture.new_from_file(item_images[current]))
		current = (current + 1) % len(item_images)
	elif event.keyval == Clutter.s or event.keyval == Clutter.S:
		coverflow.show()
	elif event.keyval == Clutter.h or event.keyval == Clutter.H:
		coverflow.hide()
	elif event.keyval == Clutter.q or event.keyval == Clutter.Q:
		Clutter.main_quit()

def destroy(*args, **kwargs):
	print "Bye Bye %s %s" % (args , kwargs)
	Clutter.main_quit()

def main(image_directory):
	print Clutter.init(sys.argv)
	stage = Clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', destroy)
	stage.set_color(Clutter.Color.new(0, 0, 0, 255))
	stage.set_title('Coverflow')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))

	coverflow = Coverflow(size=(1024, 512), item_size=(128,128), angle=70, inter_item_space=50, selection_depth=200)
	stage.add_actor(coverflow)
	stage.show()
	for image in item_images:
		coverflow.add_actor(Clutter.Texture.new_from_file(image))
	coverflow.set_position(0, 400)
	stage.connect('key-press-event', on_input, coverflow, item_images)
	Clutter.main()

if __name__ == '__main__':
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")



