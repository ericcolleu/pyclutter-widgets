#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from pyclut.basics.star import SixBranchStar
from pyclut.basics.triangle import Triangle
from pyclut.basics.rectangle import RoundRectangle
from pyclut.basics.circle import Circle, CircleChrono

def on_input(stage, event):
	if event.keyval == keysyms.q:
		clutter.main_quit()

def on_click(stage, event, chrono):
	chrono.reset()
	chrono.start()

def main(image_directory):
	stage = clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(0, 0, 0, 255))
	stage.set_title('Carrousel')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	star = SixBranchStar()
	triangle = Triangle()
	roundrect = RoundRectangle()
	circle = Circle()
	chrono = CircleChrono()
	stage.show()
	stage.add(star)
	stage.add(triangle)
	stage.add(roundrect)
	stage.add(circle)
	stage.add(chrono)
	star.set_position(400, 200)
	star.set_size(100, 100)
	triangle.set_position(500, 200)
	triangle.set_size(100, 100)
	triangle.set_texture("images/textures/Electricity.jpg")
	triangle.set_opacity(150)
	roundrect.set_position(300, 200)
	roundrect.set_size(100, 100)
	roundrect.set_texture("images/textures/cherry_wood.png")
	roundrect.set_opacity(200)
	roundrect.set_radius(25)
	circle.set_position(300, 400)
	circle.set_size(100, 100)
	circle.set_texture("images/textures/cherry_wood.png")
	circle.set_opacity(255)
	circle.radius = 50
	chrono.radius = 100
	chrono.set_position(512, 500)
	chrono.set_color("White")
	chrono.start()
	stage.connect('key-press-event', on_input)
	stage.connect("button-release-event", on_click, chrono)
	clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")




