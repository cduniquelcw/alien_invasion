class Settings():
	"""储存《外星人入侵》的所有设置的类"""

	def __init__(self):
		"""初始化游戏设置"""
		#屏幕设置
		self.screen_width = 1366
		self.screen_height = 768
		self.screen_wh =(self.screen_width,self.screen_height)
		self.bg_color = (0,191,255)
		#飞船的设置
		self.ship_speed_factor = 15
		#子弹的设置
		self.bullet_speed_factor = 1
		self.bullet_width =3
		self.bullet_height = 15
		self.bullet_color = 255,127,80
		self.bullets_allowed = 3
