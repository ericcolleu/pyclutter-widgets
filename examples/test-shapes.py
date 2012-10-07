#!/usr/bin/python

from gi.repository import Clutter
from pyclut.basics.circle import Circle, CircleChrono
from pyclut.basics.rectangle import RoundRectangle
from pyclut.basics.star import SixBranchStar
from pyclut.basics.triangle import Triangle
import glob
import os.path
import sys
import time
from pyclut.utils import get_keyval


def on_input(stage, event):
	if get_keyval(event) == Clutter.q:
		Clutter.main_quit()

def on_click(stage, event, chrono):
	chrono.reset()
	chrono.start()

def do_quit(*args):
	Clutter.main_quit()

def main(image_directory):
	Clutter.init(sys.argv)
	stage = Clutter.Stage()
	stage.set_size(1024,768)
	stage.connect('destroy', do_quit)
	stage.set_color(Clutter.Color.new(0, 0, 0, 255))
	stage.set_title('Various shapes')
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	star = SixBranchStar()
	triangle = Triangle()
	roundrect = RoundRectangle()
	circle = Circle()
	#chrono = CircleChrono()
	stage.show()
	#stage.add_actor(star)
	stage.add_actor(triangle)
	#stage.add_actor(roundrect)
	#stage.add_actor(circle)
#	stage.add_actor(chrono)
	star.set_position(400, 200)
	star.set_size(100, 100)
	triangle.set_position(500, 200)
	triangle.set_size(100, 100)
	triangle.set_texture("images/textures/Electricity.jpg")
	triangle.set_opacity(150)
	roundrect.set_position(300, 200)
	roundrect.set_size(100, 100)
	#roundrect.set_texture("images/textures/cherry_wood.png")
	roundrect.set_opacity(200)
	roundrect.set_radius(25)
	circle.radius = 50
	circle.set_position(300, 400)
	circle.set_size(100, 100)
	#circle.set_texture("images/textures/cherry_wood.png")
	circle.set_opacity(255)
#	chrono.radius = 100
#	chrono.set_position(512, 500)
#	chrono.set_color("White")
#	chrono.start()
	stage.connect('key-press-event', on_input)
#	stage.connect("button-release-event", on_click, chrono)
	Clutter.main()

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]):
		main(sys.argv[1])
	else:
		main("./images")




