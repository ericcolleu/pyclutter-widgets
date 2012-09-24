#!/usr/bin/python

from gi.repository import Clutter
from pyclut.controls.button import ImageButton, PulseButton
import os
import sys

def on_input(stage, event):
	if event.keyval == Clutter.q or event.keyval == Clutter.Q:
		Clutter.main_quit()

def do_quit(*args):
	Clutter.main_quit()

def main(image_directory):
	Clutter.init(sys.argv)
	stage = Clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', do_quit)
	stage.set_color(Clutter.Color.new(0, 0, 0, 255))
	stage.set_title('Button')
	released=Clutter.Texture.new_from_file(os.path.join(image_directory, "buttons", "ok_released.png"))
	pressed=Clutter.Texture.new_from_file(os.path.join(image_directory, "buttons", "ok_pressed.png"))
	button = ImageButton(released_background=released, pressed_background=pressed)
	pulse_button = PulseButton(background=Clutter.Texture.new_from_file(os.path.join(image_directory, "buttons", "ok_released.png")))
	stage.add_actor(button)
	stage.add_actor(pulse_button)
	button.set_position(512, 200)
	pulse_button.set_position(512, 350)
	stage.connect('key-press-event', on_input)
	stage.show()
	Clutter.main()

if __name__ == '__main__':
	main("./images")



