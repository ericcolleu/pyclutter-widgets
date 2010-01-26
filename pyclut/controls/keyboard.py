import clutter


class Key(object):
	def __init__(self, value=None, text=None):
		self.value = value
		self.text = text

	def __str__(self):
		if self.text:
			return self.text
		return ""

	def __call__(self, *args, **kwargs):
		if self.value:
			return value
		return self.text

class Modifier(Key):
	def __init__ (self, pass_to_layout, value=None, text=None):
		SpecialKey.__init__(self, value, text)
		self.pass_to_layout = pass_to_layout

class KeyFactory(object):
	def getKey(self, key):
		if isinstance(key, str):
			return Key(text=key)
		elif isinstance(key, Key):
			return key
		elif isinstance(key, list) or isinstance(key, tuple):
			return Key(text=key[0], value=key[1])
			
class KeyboardLayout:
	def __init__ (self, name, key_map=None):
		self.name = name
		self._key_map = []
		self.__key_factory = KeyFactory()
		if key_map:
			self.set_key_map(key_map)

	def set_key_map(self, key_map):
		self._key_map = []
		for line in key_map:
			key_line=[]
			for key in line:
				
		
