import clutter
from pyclut.animation import Animator

class TransitionManager(object):
	def __init__(self, stage):
		self._stage = stage
		self._anim_factory = Animator()

	def slide(self, actor_in, actor_out, direction):
		pass


