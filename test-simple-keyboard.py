#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.controls.keyboard import SimpleKeyboard, KeyboardLayout

def on_input(stage, event):
	if event.keyval == keysyms.q:
		clutter.main_quit()

def main():
	stage = clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Simple Keyboard')
# 	key_map = [
# 		["A", "B", "C",],
# 		["D", "E", "F", "G"],
# 		["H", "I",],
# 	]
	key_map = [
		["A",],
	]
	keyboard = SimpleKeyboard(layout=KeyboardLayout("layout", key_map), background=None, 
		button_released=None, button_pressed=None,
		button_size=(75,75), inter_button_space=10)
	stage.add(keyboard)
	stage.show()
	stage.connect('key-press-event', on_input)
	clutter.main()

if __name__ == '__main__':
	main()


