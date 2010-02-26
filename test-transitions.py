#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.effects.transitions import TransitionManager
from pyclut.menus.carrousel import Carrousel
from pyclut.menus.coverflow import Coverflow
from pyclut.menus.thumbnail_menu import ThumbnailMenu
global current
current=1
global menu
global menus
menu=0
menus=[]

def on_input(stage, event, item_images):
	global current
	global menu
	global menus
	if event.keyval == keysyms.Left:
		menus[menu].previous()
	elif event.keyval == keysyms.Right:
		menus[menu].next()
	elif event.keyval == keysyms.Page_Down:
		if hasattr(menus[menu], "previous_page"):
			menus[menu].previous_page()
	elif event.keyval == keysyms.Page_Up:
		if hasattr(menus[menu], "next_page"):
			menus[menu].next_page()
	elif event.keyval == keysyms.a:
		menus[menu].add(create_item(item_images[current], transition_manager))
		current = (current + 1) % len(item_images)
	elif event.keyval == keysyms.q:
		clutter.main_quit()

def on_item_clicked(item, event, transition_manager):
	global menus
	global menu
	out_menu = menus[menu]
	menu = (menu + 1)%len(menus)
	in_menu = menus[menu]
	transition_manager.slide(in_menu, out_menu)


def create_item(image, tm):
	item = clutter.Texture(image)
	item.set_reactive(True)
	item.connect("button-release-event", on_item_clicked, tm)
	return item

def main(image_directory):
	global menus
	stage = clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Carrousel')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	transition_manager = TransitionManager(stage)
	carrousel = Carrousel(size=(512,512), item_size=(128,128))
	coverflow = Coverflow(size=(512, 512), item_size=(128,128), angle=70, inter_item_space=50, selection_depth=200)
	thumbnailmenu = ThumbnailMenu(size=(300, 300), item_size=(128,128))
	coverflow.hide()
	thumbnailmenu.hide()
	menus = [carrousel, coverflow, thumbnailmenu]
	stage.add(carrousel)
	stage.add(coverflow)
	stage.add(thumbnailmenu)
	n_items = len(item_images)
	items = []
	stage.show()
	for image in item_images:
		carrousel.add(create_item(image, transition_manager))
		coverflow.add(create_item(image, transition_manager))
		thumbnailmenu.add(create_item(image, transition_manager))
	carrousel.set_position(
		stage.get_size()[0]/2-carrousel.get_size()[0]/2,
		stage.get_size()[1]/2-carrousel.get_size()[1]/2
	)
	stage.connect('key-press-event', on_input, item_images)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")


