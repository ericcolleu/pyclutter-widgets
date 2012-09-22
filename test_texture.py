#!/usr/bin/python
import sys
from gi.repository import Clutter

stage = Clutter.Stage()
stage.set_size(1024,768)
stage.connect('destroy', Clutter.main_quit)
stage.set_color(Clutter.Color(0, 0, 0, 255))
stage.set_title('texture')

stage.show()
texture = Clutter.Texture(sys.argv[0])
stage.add_actor(texture)

#print texture.get_cogl_texture()

Clutter.main()


