from pyclut.controls.panel import Panel

class UIConfigurationProxy(object):
	def __init__(self, resolution, screens, config):
		self._config = config
		if config:
			self._resolution = resolution or self._config.get_resolution()
			self._screens = self._config.get_screens()
		else:
			self._resolution = resolution or (1024, 768)
			self._screens = {}
		self._screens.update(screens or {})

	def get_resolution(self):
		return self._resolution

	def get_screens(self):
		return self._screens

	def get_nb_screen(self):
		return len(self._screens)

class UserInterface(object):
	def __init__(self, resolution=None, screens=None, config=None):
		self._config = UIConfigurationProxy(resolution, screens, config)

	def createScreen(self, name):
		pass

	def switchToScreen(self, screen_name, transition=None):
		pass

	def get_resolution(self):
		return self._config.get_resolution()

	def get_screens(self):
		return self._config.get_screens()

	def get_nb_screen(self):
		return self._config.get_nb_screen()


