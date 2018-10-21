class Settings():
	"""储存《外星人入侵》的所有设置的类"""

	def __init__(self):
		"""初始化游戏的静态设置"""
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 675
		self.screen_wh =(self.screen_width,self.screen_height)
		self.bg_color = (0,191,255)
		#飞船的设置
		self.ship_speed_factor = 3
		self.ship_limit = 3
		#子弹的设置
		self.bullet_width =3000
		self.bullet_height = 15
		self.bullet_color = 255,127,80
		self.bullets_allowed = 3
		#外星人的设置
		self.fleet_drop_speed = 8


		#以什么样的速度加快游戏节奏
		self.speedup_scale = 1.1

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""初始化随游戏进行而变化的设置"""
		self.ship_speed_factor = 3
		self.bullet_speed_factor = 15
		self.alien_speed_factor = 2

		#fleet_direction为1表示向右移动，-1表示向左移动
		self.fleet_direction = 1

	def increase_speed(self):
		"""提高速度设置"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
