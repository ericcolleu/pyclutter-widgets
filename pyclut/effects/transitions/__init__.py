import clutter
from pyclut.animation import Animator

class Direction:
	LEFT = "left"
	RIGHT = "right"
	TOP = "top"
	BOTTOM = "bottom"

class TransitionManager(object):
	def __init__(self, stage):
		self._stage = stage
		self._stage_size = stage.get_size()
		self._stage_center = (self._stage_size[0]/2, self._stage_size[1]/2)
		self._anim_factory = Animator()

	def slide(self, actor_in, actor_out, direction=Direction.LEFT, final_position=None, duration=1.0):
		actor_out_width, actor_out_height = actor_out.get_size()
		final_position = final_position or (self._stage_center[0]-actor_out_width/2,self._stage_center[1]-actor_out_height/2)
		if direction == Direction.LEFT:
			print actor_in, actor_out
			actor_in.set_position(self._stage_size[0]+actor_in.get_size()[0]+10, final_position[1])
		actor_in.show()
		anim_in = self._anim_factory.createMoveAnimation(final_position)
		anim_in.apply(actor_in)
		anim_out = self._anim_factory.createMoveAnimation(
			(-actor_out.get_size()[0]-10, actor_out.get_position()[1])
		)
		anim_out.apply(actor_out)
		anim_out.connect("completed", self._on_anim_completed, actor_out)
		anim_in.start()
		anim_out.start()

	def _on_anim_completed(self, event, actor_out):
		actor_out.hide()

