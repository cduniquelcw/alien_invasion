class Settings():
	"""储存《外星人入侵》的所有设置的类"""

	def __init__(self):
		"""初始化游戏设置"""
		#屏幕设置
		self.screen_width = 1366
		self.screen_height = 768
		self.screen_wh =(self.screen_width,self.screen_height)
		self.bg_color = (0,191,255)
