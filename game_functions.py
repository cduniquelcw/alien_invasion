import sys

import pygame

def check_events():
	#监视键盘和鼠标
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()

def update_screen(ai_settings,screen,ship):
	"""更新屏幕上的图像，并切换到新屏幕"""
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	#让屏幕可见
	pygame.display.flip()
