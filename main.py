# imports

import pygame
import math
import random
import time

from collections import deque

from mapgen import road_images
from mapgen2 import mapgenerate

# color definitions

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
KEY = (100,100,100) # invisible color

# variable definitions

done = False

distance = 0

scroll_speed = 10

clock = pygame.time.Clock()

current_state = 1

max_speed = 10

# general function definitions

def get_image(self, x, y, width, height):
        
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(KEY)
        return image

class SpriteSheet(object):

    def __init__(self, file_name):

        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(KEY)
        return image

def background_check():

    for background in all_backgrounds_list:
        if background.rect.y >= 0:
            all_backgrounds_list.remove(background)
            all_sprites_list.remove(background)
            background = Background(current_state)

def state_check():

    global current_state
    if distance > 100:
        rand_1 = random.randint(1,100)
        if rand_1 > 80:
            current_state = 2

# class definitions

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        
        self.width = 80
        self.height = 100

        player = SpriteSheet("sprites/spritesheet.png")
        self.image = player.get_image(0,0,self.width,self.height)
        self.rect = self.image.get_rect()

        self.xspeed = 0
        self.yspeed = 0
        self.speed = 4

        self.W = False
        self.A = False
        self.S = False
        self.D = False 

        self.bullets = 2
         
    def update(self):

        # vertical movement checks

        if self.W == False and self.S == False:
            self.yspeed = 0
        elif self.W == True and self.S == True:
            self.yspeed = 0
        elif self.W == True and self.S == False:
            self.yspeed = -abs(self.speed)
        elif self.W == False and self.S == True:
            self.yspeed = abs(self.speed)
        
        # horizontal movement checks

        if self.A == False and self.D == False:
            self.xspeed = 0
        elif self.A == True and self.D == True:
            self.xspeed = 0
        elif self.A == True and self.D == False:
            self.xspeed = -self.speed
        elif self.A == False and self.D == True:
            self.xspeed = self.speed

        global player_mask_image

        # location update
        
        global overlap_area
        global overlap_area2
        global scroll_speed

        if overlap_area != 6310 and overlap_area2 != 6310:
            if scroll_speed > 1:
                scroll_speed -= 0.1

        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        # check for screen borders

        if self.rect.x + self.width >= screen_width:
            self.rect.x = screen_width - self.width
        if self.rect.x < 0:
            self.rect.x = 0
        
        if self.rect.y + self.height >= screen_height:
            self.rect.y = screen_height - self.height
        if self.rect.y <= 0:
            self.rect.y = 0

class Background(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1024, 1536])
        if current_state == 1:
            background = SpriteSheet("sprites/backgrounds/grass1.png")
        self.image = background.get_image(0,0,1024,1536)
        self.rect = self.image.get_rect()
        self.y_float = 0

    def update(self):

        global scroll_speed
        self.y_float += scroll_speed
        self.rect.y = round(self.y_float)
        if self.rect.y > 0:
            self.rect.y = -768
            self.y_float = -768

class Road(pygame.sprite.Sprite):

    def __init__(self, y_position):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1024, 768])
        self.gen()
        self.rect = self.image.get_rect()

        self.nextdone = False

        self.num = 0
        self.y_float = y_position

    def update(self):
        global scroll_speed
        self.y_float += scroll_speed
        self.rect.y = round(self.y_float)

        if self.rect.y >= screen_height:
            highest_y = min(road.y_float for road in all_roads_list if road != self)
            self.y_float = highest_y - 768
            self.rect.y = round(self.y_float)
            self.gen()

    def gen(self):

        global map_list

        if len(map_list) == 0:
            map_list.extend(mapgenerate("1m",10))

        current_road = map_list.popleft()
        
        # road_images = {
        #     "1m": "sprites/roads/1m.png",
        #     "1m2lr": "sprites/roads/1m2lr.png",
        #     "2lr": "sprites/roads/2lr.png",
        #     "2lr1m": "sprites/roads/2lr1m.png"
        #     "
        # }

        global road_images

        background = SpriteSheet(road_images[current_road])
        self.image = background.get_image(0,0,1024,780)

class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 20])
        bullet = SpriteSheet("sprites/spritesheet.png")
        self.image = bullet.get_image(80,0,10,20)
        self.rect = self.image.get_rect()

        global scroll_speed
        self.speed = scroll_speed

    def update(self):

        global max_speed
        self.rect.y -= max_speed

# screen definition

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Action Fighter Game")

# map generation function

map_list = deque()
# map_list.extend([1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 1, 1, 1, 1, 1])
map_list.extend(mapgenerate("1m", 10))

# print(map_list)

# sprite group definitions

all_sprites_list = pygame.sprite.Group()
all_backgrounds_list = pygame.sprite.Group()
all_players_list = pygame.sprite.Group()
all_roads_list = pygame.sprite.Group()
all_bullets_list = pygame.sprite.Group()

# layer group definitions

# 1 = bottom, 10 = top

layer1 = pygame.sprite.Group() # background
layer2 = pygame.sprite.Group() # road
layer3 = pygame.sprite.Group()
layer4 = pygame.sprite.Group()
layer5 = pygame.sprite.Group() # bullets
layer6 = pygame.sprite.Group() # player
layer7 = pygame.sprite.Group()
layer8 = pygame.sprite.Group()
layer9 = pygame.sprite.Group()
layer10 = pygame.sprite.Group() 

# sprite definitions

##player definition

player = Player(BLUE, 100, 100)
all_sprites_list.add(player)
all_players_list.add(player)
layer6.add(player)
player.rect.x = 472
player.rect.y = 534

## background definition

background = Background()
all_sprites_list.add(background)
all_backgrounds_list.add(background)
layer1.add(background)
background.rect.x = 0
background.rect.y = 0

## road definition

road1 = Road(0)
# all_sprites_list.add(road)
# all_roads_list.add(road)
# layer2.add(road)
# road.rect.x = 0
# road.rect.y = 0
# road.y_float = 0
# road.num = 1
# road.gen()

road2 = Road(-768)
# all_sprites_list.add(road2)
# all_roads_list.add(road2)
# layer2.add(road2)
# road2.rect.x = 0
# road2.rect.y = -768
# road2.y_float = -768
# road2.num = 2
# road2.gen()

all_sprites_list.add(road1, road2)
all_roads_list.add(road1, road2)
layer2.add(road1, road2)

# invisible mouse

pygame.mouse.set_visible(False)

# file definitions

pygame.init()

# main code

# print(mapgenerate("2lr", 10))

while not done:
    
    # input code
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.W = True
            elif event.key == pygame.K_s:
                player.S = True
            elif event.key == pygame.K_a:
                player.A = True
            elif event.key == pygame.K_d:
                player.D = True
            elif event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE and distance > 10:

                if player.bullets == 1:

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 35
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer5.add(bullet)

                elif player.bullets == 2:

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 60
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer5.add(bullet)

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 10
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer5.add(bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.W = False
            elif event.key == pygame.K_s:
                player.S = False
            elif event.key == pygame.K_a:
                player.A = False
            elif event.key == pygame.K_d:
                player.D = False

    # sprite masks
    
    player_mask = pygame.mask.from_surface(player.image)
    player_mask_image = player_mask.to_surface()

    # road 1 mask
    road_mask = pygame.mask.from_surface(road1.image)
    road_mask_image = road_mask.to_surface()
    road_mask_image.set_colorkey(BLACK)

    # road 2 mask
    road_mask2 = pygame.mask.from_surface(road2.image)
    road_mask_image2 = road_mask2.to_surface()
    road_mask_image2.set_colorkey(BLACK)

    # road offsets

    offset_x = road1.rect.x - player.rect.x
    offset_y = road1.rect.y - player.rect.y
    overlap_area = player_mask.overlap_area(road_mask, (offset_x, offset_y))

    offset_x2 = road2.rect.x - player.rect.x
    offset_y2 = road2.rect.y - player.rect.y
    overlap_area2 = player_mask.overlap_area(road_mask2, (offset_x2, offset_y2))

    #combined_road_surface = pygame.Surface((screen_width, screen_height * 2))
    #combined_road_surface.fill((0,0,0))
    #combined_road_surface.blit(road.image, road.rect.topleft)
    #combined_road_surface.blit(road2.image, road2.rect.topleft)

    #combined_road_mask = pygame.mask.from_surface(combined_road_surface)
    #combined_road_mask_image = combined_road_mask.to_surface()

    #overlap_area = player_mask.overlap_area(combined_road_mask, (0, 0))

    overlap_area = player_mask.overlap_area(road_mask, (road1.rect.x - player.rect.x, road1.rect.y - player.rect.y))
    overlap_area2 = player_mask.overlap_area(road_mask2, (road2.rect.x - player.rect.x, road2.rect.y - player.rect.y))

    # print(f"Road 1: y={road1.rect.y}, y_float={road1.y_float}")
    # print(f"Road 2: y={road2.rect.y}, y_float={road2.y_float}")
    # print(f"Map List: {list(map_list)}")

    # distance increment

    distance += int(scroll_speed)

    # print(int(distance // 100))

    # state check

    state_check()
    
    # road update

    #for road in all_roads_list:
    #    if road.rect.y >= 768:
    #        road.rect.y = - 768
    #        road.gen()

    # sprite updates

    player.update()

    background.update()

    for road in all_roads_list:
        road.update()

    for bullet in all_bullets_list:
        bullet.update()

    # scroll speed update

    if scroll_speed < max_speed:
        scroll_speed = round(scroll_speed + 0.05, 3)
    
    #print(scroll_speed)

    #print(road.rect.y, road.rect.x)
    #print(road2.rect.y, road2.rect.x)

    # screen drawing

    screen.fill(BLACK)

    layer1.draw(screen)
    layer2.draw(screen)
    layer3.draw(screen)
    layer4.draw(screen)
    layer5.draw(screen)
    layer6.draw(screen)
    layer7.draw(screen)
    layer8.draw(screen)
    layer9.draw(screen)
    layer10.draw(screen)

    # screen.blit(combined_road_mask_image, (0,0))
    # screen.blit(player_mask_image, (0, 0))
    # screen.blit(road_mask_image, road1.rect.topleft)
    # screen.blit(road_mask_image2, road2.rect.topleft)
    # screen.blit(background_mask_image, (0,0))

    # screen update

    clock.tick(60)

    pygame.display.flip()

pygame.quit()