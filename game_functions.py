import sys

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""相应按键"""
	if event.key == pygame.K_RIGHT:
		#向右移动飞船
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def check_keyup_events(event,ship):
	"""相应松开按键"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
	

def check_events(ai_settings,screen,ship,bullets):
	#监视键盘和鼠标
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#让屏幕可见
	pygame.display.flip()

def update_bullets(bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	bullets.update()
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def fire_bullet(ai_settings,screen,ship,bullets):
	"""如果还没达到限制，就发射一颗子弹"""
	#创建新子弹，并将其加入到编组bullets中
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings,screen,ship)
			bullets.add(new_bullet)

		

def get_number_aliens_x(ai_settings,alien_width):
	"""计算一行可容纳多少个外星人"""
	available_spece_x = ai_settings.screen_width-2*alien_width
	number_aliens_x = int(available_spece_x/(2*alien_width))
	return number_aliens_x

def creat_alien(ai_settings,screen,aliens,alien_number,number_rows):
	"""创建一个外星人,并将其放在当前行"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien_width *number_rows
	aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	#外星人列数
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	#外星人行数
	number_rows = get_number_rows(
		ai_settings,ship.rect.height,alien.rect.height)
	
	#创建外星人群
	for number_row in range(number_rows):
		for alien_number in range(number_aliens_x):
			creat_alien(ai_settings,screen,aliens,alien_number,number_row)

def  get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_spece_y = (
		ai_settings.screen_height - (3 * alien_height)- ship_height)
	number_rows = int(available_spece_y/alien_height/2)
	return number_rows

def update_aliens(aliens):
	"""更新外星人群中所有外星人的位置"""
	aliens.update()