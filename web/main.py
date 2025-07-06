import pygame
from pygame.locals import *
import random
import time

pygame.init()

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('MAX VERSTAPPEN VS ALIEN')

gray = (50, 50, 50)
green = (30, 100, 30)
red = (150, 0, 0)
white = (200, 200, 200)
yellow = (200, 182, 0)

road_width = 300
marker_width = 10
marker_height = 50

left_lane = 125
center_lane = 225
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

lane_marker_move_y = 0

player_x = 250
player_y = 400

clock = pygame.time.Clock()
fps = 150

gameover = True  
speed = 1
score = 0
start_time = 0

collision_sound = pygame.mixer.Sound('img/collide.wav')
switch_lane_sound = pygame.mixer.Sound('img/laneswitch.wav')

pygame.mixer.music.load('img/bgsong.wav')
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)

player_car_image = pygame.transform.scale(pygame.image.load('img/playercar.png'), (50, 100))
enemy_car_image = pygame.transform.scale(pygame.image.load('img/enemycar.png'), (50, 100))

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        super().__init__(player_car_image, x, y)
        
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

player = PlayerVehicle(player_x, player_y)
player_group.add(player)

running = True
while running:
    
    clock.tick(fps)
    
    if not gameover:
        if score > 500:
            speed = 2  
        elif score > 1000:
            speed = 4 
        elif score > 1300:
            speed = 5 
        elif score > 1500:
            speed = 6
        elif score > 1600:
            speed = 9
        elif score > 1700:
            speed = 10   
        else:
            speed = 1
        
        fps = 150 + int(score / 1) 
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        if gameover:  
            if event.type == MOUSEBUTTONDOWN:
                if 150 < event.pos[0] < 350 and 200 < event.pos[1] < 300:
                    gameover = False
                    score = 0
                    start_time = time.time()
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
        else:  
            if event.type == KEYDOWN:
                if event.key == K_LEFT and player.rect.center[0] > left_lane:
                    player.rect.x -= 100
                    switch_lane_sound.play()  
                elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                    player.rect.x += 100
                    switch_lane_sound.play()  
                
    if not gameover:
        screen.fill(green)
        
        pygame.draw.rect(screen, gray, road)
        
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)
        
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            if y != height // 2: 

                pass
        
        player_group.draw(screen)
        
        if len(vehicle_group) < 2:
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
                    
            if add_vehicle:
                lane = random.choice(lanes)
                vehicle = Vehicle(enemy_car_image, lane, height / -2)
                vehicle_group.add(vehicle)
        
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            
            if vehicle.rect.left < left_lane:
                vehicle.rect.left = left_lane
            elif vehicle.rect.right > right_lane:
                vehicle.rect.right = right_lane
            
            if vehicle.rect.top >= height:
                vehicle.kill()
        
        elapsed_time = time.time() - start_time
        score = int(elapsed_time * 10)  
        
        vehicle_group.draw(screen)
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Score: ' + str(score), True, white)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 10) 
        screen.blit(text, text_rect)
        
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            collision_sound.play() 

    if gameover:
        pygame.draw.rect(screen, red, (150, 200, 200, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('MAX CRASH MAX NO WIN', True, white)
        text_rect = text.get_rect()
        text_rect.center = (250, 250)
        screen.blit(text, text_rect)
            
    pygame.display.update()

pygame.quit()
