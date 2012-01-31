from gi.repository import  Clutter, Cogl

class DoubleFaceTexture(Clutter.Group):
	__gtype_name__ = 'DoubleFaceTexture'

	def __init__(self, front, back):
		Clutter.Group.__init__(self)
		self._front = Clutter.Texture(front)
		self._back = Clutter.Texture(back)
		self._back.set_rotation(Clutter.AlignAxis.Y_AXIS, 180, self._back.get_width()/2, 0, 0)
		self.add(self._back)
		self.add(self._front)

	def do_paint(self):
		cull = Cogl.get_backface_culling_enabled()
		Cogl.set_backface_culling_enabled(True)
		Clutter.Group.do_paint(self)
		Cogl.set_backface_culling_enabled(cull)

