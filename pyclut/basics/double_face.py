import clutter
import gobject
from clutter import cogl

class DoubleFaceTexture(clutter.Group):
	__gtype_name__ = 'DoubleFaceTexture'

	def __init__(self, front, back):
		clutter.Group.__init__(self)
		self._front = clutter.Texture(front)
		self._back = clutter.Texture(back)
		self._back.set_rotation(clutter.Y_AXIS, 180, self._back.get_width()/2, 0, 0)
		self.add(self._back)
		self.add(self._front)

	def do_paint(self):
		cull = cogl.get_backface_culling_enabled()
		cogl.set_backface_culling_enabled(True)
		clutter.Group.do_paint(self)
		cogl.set_backface_culling_enabled(cull)

