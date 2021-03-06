import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self,ai_settings,screen):
		"""初始化飞船并设置其初始位置"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#加载飞船图像并获取其外矩形
		self.image = pygame.image.load('images/Guaiguai.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.center_ship()

		#centerx中存储小数
		self.center = float(self.rect.centerx)

		#移动标志
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		#根据移动标志调整飞船位置
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > 0:
			self.rect.bottom -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.rect.bottom += self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)

	def center_ship(self):
		"""重置飞船在屏幕中"""
		self.center = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		