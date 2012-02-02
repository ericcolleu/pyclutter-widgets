#!/usr/bin/python

from gi.repository import Clutter, GObject
from pyclut.animation import Animator, TurnAroundAnimation
import glob
import os.path
import pygtk
pygtk.require('2.0')


global current_anim
current_anim=0
global anims_label
anims_label = ["Move", "Rotate", "Scale", "Opacify", "Depth"]
global label

def on_input(stage, event):
	if event.keyval == Clutter.keysyms.q:
		Clutter.main_quit()

def on_button_press(stage, event, factory, actor, _):
	global label
	global current_anim
	global anims_label
	anims = []
	if event.get_button() == 3:
		current_anim = (current_anim + 1) % len(anims_label)
		label.set_text(anims_label[current_anim])
	else:
		if current_anim == 0:
			anims.append(factory.createScaleAnimation(1.0, 1.0))
			anims.append(factory.createOpacityAnimation(255))
			anims.append(factory.createMoveAnimation((event.x, event.y)))
		elif current_anim == 1:
			anims.append(factory.createScaleAnimation(1.0, 1.0))
			anims.append(factory.createOpacityAnimation(255))
			anims.append(factory.createRotateAnimation(360))
		elif current_anim == 2:
			anims.append(factory.createOpacityAnimation(255))
			anims.append(factory.createScaleAnimation(2.0, 2.0))
		elif current_anim == 3:
			anims.append(factory.createScaleAnimation(1.0, 1.0))
			anims.append(factory.createOpacityAnimation(100))
		elif current_anim == 4:
			anims.append(factory.createScaleAnimation(1.0, 1.0))
			anims.append(factory.createOpacityAnimation(255))
			anims.append(factory.createDepthAnimation(100))
	[anim.apply(actor) for anim in anims]
	[anim.start() for anim in anims]

def anim_done(*args):
	print "Yessss !!!", args

def do_quit(*args):
	Clutter.main_quit()

def main(image_directory):
	global label
	global current_anim
	global anims_label
	stage = Clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', do_quit)
	stage.set_color(Clutter.Color.new(255, 255, 255, 255))
	stage.set_title('Animations')
	factory = Animator()
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	label = Clutter.Text()
	label.set_text(anims_label[current_anim])
	actor = Clutter.Texture.new_from_file(item_images[0])
	stage.add_actor(label)
	stage.add_actor(actor)
	actor.set_position(500, 500)
	anim = TurnAroundAnimation(center=(500,500), radius=300, angle=360, tilt=(360,360,300), duration=500, style=Clutter.AnimationMode.LINEAR)
	anim.apply(actor)
	anim.start()
	stage.connect('button-press-event', on_button_press, factory, actor, "")
	stage.connect('key-press-event', on_input)
	stage.show()
	Clutter.main()

if __name__ == '__main__':
	main("./images")



