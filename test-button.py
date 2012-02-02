#!/usr/bin/python

from gi.repository import Clutter
import glob, time
import os.path
from pyclut.controls.button import ImageButton, PulseButton

def on_input(stage, event):
	if event.keyval == Clutter.keysyms.q:
		Clutter.main_quit()

def main(image_directory):
	stage = Clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', Clutter.main_quit)
	stage.set_color(Clutter.Color(0, 0, 0, 255))
	stage.set_title('Button')
	released=Clutter.Texture(os.path.join(image_directory, "buttons", "ok_released.png"))
	pressed=Clutter.Texture(os.path.join(image_directory, "buttons", "ok_pressed.png"))
	button = ImageButton(released_background=released, pressed_background=pressed)
	pulse_button = PulseButton(background=Clutter.Texture(os.path.join(image_directory, "buttons", "ok_released.png")))
	stage.add(button)
	stage.add(pulse_button)
	button.set_position(512, 200)
	pulse_button.set_position(512, 350)
	stage.connect('key-press-event', on_input)
	stage.show()
	Clutter.main()

if __name__ == '__main__':
	main("./images")



