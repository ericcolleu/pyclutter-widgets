#!/usr/bin/python

from gi.repository import Clutter

import glob
import os.path
from pyclut.menus.carrousel import Carrousel, TextCarrousel
from pyclut.basics.rectangle import RoundRectangle
global current
current=1

def on_input(stage, event, carrousel, textcarrousel, item_images):
	global current
	if event.keyval == Clutter.KEY_Left:
		carrousel.previous()
	elif event.keyval == Clutter.KEY_Right:
		carrousel.next()
	elif event.keyval == Clutter.KEY_Up:
		textcarrousel.previous()
	elif event.keyval == Clutter.KEY_Down:
		textcarrousel.next()
	elif event.keyval == Clutter.a or event.keyval == Clutter.A:
		carrousel.add_actor(Clutter.Texture(item_images[current]))
		current = (current + 1) % len(item_images)
	elif event.keyval == Clutter.s or event.keyval == Clutter.S:
		carrousel.show()
	elif event.keyval == Clutter.h or event.keyval == Clutter.H:
		carrousel.hide()
	elif event.keyval == Clutter.q or event.keyval == Clutter.Q:
		Clutter.main_quit()

def main(image_directory):
	stage = Clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', Clutter.main_quit)
	stage.set_color(Clutter.Color(0, 0, 0, 255))
	stage.set_title('Carrousel')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	text_selector = RoundRectangle()
	text_selector.set_color("Blue")
	text_selector.set_opacity(150)
	text_selector.set_size(200, 40)
	texts = [
		"Item0",
		"Item1",
		"Item2",
		"Item3",
		"Item4",
		"Item5",
		"Item6",
		"Item7",
	]
	carrousel = Carrousel(size=(512,512), item_size=(128,128), fade_ratio=50, tilt=(60.0, 0.0, 0.0))
	textcarrousel = TextCarrousel(
		font="Trebuchet MS 24",
		item_color="White",
		selected_item_color="Black",
		size=(256,256),
		item_size=(256,256),
		fade_ratio=60,
		tilt=(0.0, 270.0, 90.0),
		children=texts
	)
	stage.add_actor(carrousel)
	stage.add_actor(textcarrousel)
	stage.add_actor(text_selector)
	stage.show()
	for rank, image in enumerate(item_images):
		text = Clutter.Text("Courrier New 24 px")
		text.set_text("%d" % rank)
		text.set_color(Clutter.Color.from_string("White"))
		item = Clutter.Group()
		item.add_actor(Clutter.Texture(image))
#		item.add_actor(ReflectedItem(Clutter.Texture(image)))
		item.add_actor(text)
		carrousel.add_actor(item)

	carrousel.set_position(
		stage.get_size()[0]/2-carrousel.get_size()[0]/2,
		stage.get_size()[1]/2-carrousel.get_size()[1]/2
	)
	textcarrousel.set_position(750, 330)
	text_selector.set_position(700, 300)
	stage.connect('key-press-event', on_input, carrousel, textcarrousel, item_images)
	Clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")

