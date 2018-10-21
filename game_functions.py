import sys
from time import sleep
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
	

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
	#监视键盘和鼠标
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,
				play_button,ship,aliens,bullets,mouse_x,mouse_y)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	#如果游戏处于非活动状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()	
	#让屏幕可见
	pygame.display.flip()

	


def update_bullets(ai_settings,screen,ship,aliens,bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	bullets.update()
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	"""相应子弹和外星人的碰撞"""
	#删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)

	if len(aliens) == 0:
		#删除现有的子弹,加快节奏，并创建新的一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,ship,aliens)
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

def create_alien(ai_settings,screen,aliens,alien_number,number_rows):
	"""创建一个外星人,并将其放在当前行"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien_width *number_rows
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
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
			create_alien(ai_settings,screen,aliens,alien_number,number_row)

def  get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_spece_y = (
		ai_settings.screen_height - (3 * alien_height)- ship_height)
	number_rows = int(available_spece_y/alien_height/2)
	return number_rows

def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移，并改变移动方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	#检测外星人和飞船间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	"""响应被外星人撞到的飞船"""
	#将ship_left减1
	if stats.ships_left > 0:
		stats.ships_left -= 1
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		#创建一群新的外星人，并重置飞船到屏幕底部中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		#暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_play_button(
	ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""在玩家单击Play按钮时开始新游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()

		#隐藏光标
		pygame.mouse.set_visible(False)

		#重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True

		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		#创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()


