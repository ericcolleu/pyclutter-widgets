#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.controls.button import ImageButton

def on_input(stage, event):
	if event.keyval == keysyms.q:
		clutter.main_quit()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Button')
	released=clutter.Texture(os.path.join(image_directory, "buttons", "ok_released.png"))
	pressed=clutter.Texture(os.path.join(image_directory, "buttons", "ok_pressed.png"))
	button = ImageButton(released_background=released, pressed_background=pressed)
	stage.add(button)
	button.set_position(512, 200)
	stage.connect('key-press-event', on_input)
	stage.show()
	clutter.main()

if __name__ == '__main__':
	main("./images")



