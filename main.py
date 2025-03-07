# imports

import pygame
import math
import random
import time
from collections import deque

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

scroll_speed = 0

clock = pygame.time.Clock()

current_state = 1

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
    for background in all_backgrounds_list():
        if background.rect.y >= 0:
            all_backgrounds_list.remove(background)
            all_sprites_list.remove(background)
            background = Background(current_state)

def road_check():
    for road in all_roads_list():
        if road.rect.y >= 0:
            all_roads_list.remove(road)
            all_sprites_list.remove(road)
            road = Road(current_state)

def state_check():
    global current_state
    if distance > 100:
        rand_1 = random.randint(1,100)
        if rand_1 > 80:
            current_state = 2

def generate_map(map_list):
    for x in range(1,5):
        map_list.appendleft(1)
    map_list.appendleft(2)
    map_list.appendleft(3)
    for x in range(1,5):
        map_list.appendleft(4)
    map_list.appendleft(5)
    map_list.appendleft(6)
    for x in range(1,5):
        map_list.appendleft(1)


# class definitions

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        player = SpriteSheet("spritesheet.png")
        self.width = 80
        self.height = 100
        self.image = player.get_image(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 4
        self.W = False
        self.A = False
        self.S = False
        self.D = False
         
    def update(self):

        # vertical movement checks

        if self.W == False and self.S == False:
            self.yspeed = 0
        elif self.W == True and self.S == True:
            self.yspeed = 0
        elif self.W == True and self.S == False:
            self.yspeed = -self.speed
        elif self.W == False and self.S == True:
            self.yspeed = self.speed
        
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
        global road_mask_image

        # location update
        
        global overlap_area
        global scroll_speed

        if overlap_area != 6310:
            if scroll_speed > 1:
                scroll_speed -= 0.1
            if self.yspeed > 0:
                self.yspeed =- 1

        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        # check for screen borders

        # if self.rect.x + self.width >= screen_width - 228:
            # self.rect.x = screen_width - self.width - 228
        # if self.rect.x <= 228:
            # self.rect.x = 228
        
        if self.rect.y + self.height >= screen_height:
            self.rect.y = screen_height - self.height
        if self.rect.y <= 0:
            self.rect.y = 0

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1024, 1536])
        if current_state == 1:
            background = SpriteSheet("grass1.png")
        self.image = background.get_image(0,0,1024,1536)
        self.rect = self.image.get_rect()
    def update(self):
        global scroll_speed
        self.rect.y += scroll_speed
        if self.rect.y > 0:
            self.rect.y = -768

class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([1024, 1536])
        background = SpriteSheet("road.png")
        self.image = background.get_image(0,0,1024,1536)
        self.rect = self.image.get_rect()
    def update(self):
        global scroll_speed
        self.rect.y += scroll_speed
        if self.rect.y > 0:
            self.gen()
            self.rect.y = -768
    def gen(self):
        next = map_list.pop()
        if next == 1:
            background = SpriteSheet("road.png")
            self.image = background.get_image(0,0,1024,1536)
        elif next == 2:
            background = SpriteSheet("road2.png")
            self.image = background.get_image(0,0,1024,1536)
        elif next == 3:
            background = SpriteSheet("road3.png")
            self.image = background.get_image(0,0,1024,1536)
        elif next == 4:
            background = SpriteSheet("road4.png")
            self.image = background.get_image(0,0,1024,1536)
        elif next == 5:
            background = SpriteSheet("road5.png")
            self.image = background.get_image(0,0,1024,1536)
        elif next == 6:
            background = SpriteSheet("road6.png")
            self.image = background.get_image(0,0,1024,1536)

# screen definition

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Action Fighter Game")

# map generation function

map_list = deque()
generate_map(map_list)

# sprite group definitions

all_sprites_list = pygame.sprite.Group()
all_backgrounds_list = pygame.sprite.Group()
all_players_list = pygame.sprite.Group()
all_roads_list = pygame.sprite.Group()

# layer group definitions

# 1 = bottom, 10 = top

layer1 = pygame.sprite.Group() # background
layer2 = pygame.sprite.Group()
layer3 = pygame.sprite.Group()
layer4 = pygame.sprite.Group()
layer5 = pygame.sprite.Group()
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
background.rect.y = -768

## road definition

road = Road()
all_sprites_list.add(road)
all_roads_list.add(road)
layer2.add(road)
road.rect.x = 0
road.rect.y = 0

# invisible mouse

pygame.mouse.set_visible(False)

# file definitions

pygame.init()

# main code

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
    
    # background_mask = pygame.mask.from_surface(background.image)
    # background_mask_image = background_mask.to_surface()

    player_mask = pygame.mask.from_surface(player.image)
    player_mask_image = player_mask.to_surface()

    road_mask = pygame.mask.from_surface(road.image)
    road_mask_image = road_mask.to_surface()

    overlap_area = player_mask.overlap_area(road_mask, (road.rect.x - player.rect.x, road.rect.y - player.rect.y))

    print(overlap_area)

    # distance increment

    distance += 1

    # state check

    state_check()
    
    # sprite updates

    player.update()

    background.update()

    road.update()

    # scroll speed update

    if scroll_speed < 10:
            scroll_speed += 0.05

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

    # screen.blit(player_mask_image, (0, 0))
    # screen.blit(road_mask_image, (0,0))
    # screen.blit(background_mask_image, (0,0))

    # screen update

    clock.tick(60)

    pygame.display.flip()

pygame.quit()