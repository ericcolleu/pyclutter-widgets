#!/usr/bin/python

import clutter

import glob, time
import os.path
from clutter import keysyms
from widget.animation import Animator, MoveAndRotateAnimation
global current_anim
current_anim=0
global anims_label
anims_label = ["Move", "Rotate", "Scale", "Opacify",]

def on_input(stage, event):
	if event.keyval == keysyms.q:
		clutter.main_quit()

def on_button_press(stage, event, factory, actor, label):
	global current_anim
	global anims_label
	anims = []
	if event.button == 3:
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
	[anim.apply(actor) for anim in anims]
	[anim.start() for anim in anims]

def main(image_directory):
	global current_anim
	global anims_label
	stage = clutter.Stage()
	stage.set_size(1024, 768)
	stage.connect('destroy', clutter.main_quit)
	stage.set_color(clutter.Color(255, 255, 255, 255))
	stage.set_title('Animations')
	factory = Animator()
	item_images = glob.glob(os.path.join(image_directory, "*.png"))
	label = clutter.Text()
	label.set_text(anims_label[current_anim])
	actor = clutter.Texture(item_images[0])
	stage.add(label)
	stage.add(actor)
	actor.set_position(500, 500)
	stage.connect('button-press-event', on_button_press, factory, actor, label)
	stage.connect('key-press-event', on_input)
	stage.show()
	clutter.main()

if __name__ == '__main__':
	main("./images")



