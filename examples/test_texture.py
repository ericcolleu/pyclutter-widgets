#!/usr/bin/python
import sys
from gi.repository import Clutter

def do_quit(*args):
	Clutter.main_quit()

Clutter.init(sys.argv)
stage = Clutter.Stage()
stage.set_size(1024,768)
stage.connect('destroy', do_quit)
stage.set_color(Clutter.Color.new(0, 0, 0, 255))
stage.set_title('texture')

stage.show()
texture = Clutter.Texture.new_from_file(sys.argv[1])
stage.add_actor(texture)

#print texture.get_cogl_texture()

Clutter.main()


