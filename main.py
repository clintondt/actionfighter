# imports

import pygame
import math
import random
import time

from collections import deque

from mapgen import road_images
from mapgen import map_graph
from mapgen import start_map_graph
from mapgen import straight_map_graph
from mapgen2 import mapgenerate

# color definitions

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
KEY = (100,100,100) # invisible color

# variable definitions

done = False # tracks if game running

distance = 0 # disntance the car has gon

clock = pygame.time.Clock() # initialise clock

max_speed = 10 # max scroll speed, in pixels per frame, breaks if > 10
scroll_speed = 0 # current speed of the map

roads = 0 # number of roads which have been generated

sect = 0 # which screen is currently displayed, info in onenote notes
mode = 1 # game mode, info in onenote notes
current_state = 1 # background image

dead = False # tracks if the player has died
explosion_timer = pygame.USEREVENT + 1

car_timer = 0 # amount of frames since a car has spawned
car_gap = 150 # amount of frames before the chance of a car spawning resets
car_spawn = 60 # 1 in x chance of spawning a car every frame

# general function definitions

def get_image(self, x, y, width, height): # returns a section of an image
        
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(KEY)
        return image

class SpriteSheet(object): # loads an image to use with get_image

    def __init__(self, file_name):

        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(KEY)
        return image

def background_check(): # ensures background contantly scrolls

    for background in all_backgrounds_list:
        if background.rect.y >= 0:
            all_backgrounds_list.remove(background)
            all_sprites_list.remove(background)
            background = Background(current_state)

def state_check(): # doesnt currently do anything

    global current_state
    if distance > 100:
        rand_1 = random.randint(1,100)
        if rand_1 > 80:
            current_state = 2

def set_mode(m): # sets mode variable to input
    global mode
    mode = m

def sect_check(): # decides which section to generate next

    global sect
    global roads

    if roads < 5:
        sect = 0
    elif roads < 50:
        sect = 1
    else:
        sect = 2

def car_gen(): # randomly generates enemy cars

    global car_timer
    global car_gap

    if car_timer > car_gap:

        r = random.randint(0, car_spawn)

        if r == 0:
            dir = random.randint(1,2)
            if dir == 1:
                car = Car("car1", "up")
                car.rect.y = screen_height
            else:
                car = Car("car1", "down")
                car.rect.y = -100
            all_sprites_list.add(car)
            all_cars_list.add(car)
            all_enemies_list.add(car)
            layer0_6.add(car)
            car.rect.x = random.randint(224, 712)
            car_timer = 0

    # car_timer increments every frame
    # car_gap is the mininum frames between two cars spawning
    # car_spawn is the change of a car spawning on a certain frame
    # car_timer resets when a car is spawned
    # r randomly decides the cars direction, 1 = up, 2 = down
    # the car's x position is randomly decided, in the width of 1m

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

        self.bullets = 2 # amount of bullets the player is able to shoot
         
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
        global roads
        self.y_float += scroll_speed
        self.rect.y = round(self.y_float)

        if self.rect.y >= screen_height:
            highest_y = min(road.y_float for road in all_roads_list if road != self)
            self.y_float = highest_y - 768
            self.rect.y = round(self.y_float)
            self.gen()
            roads += 1

    def gen(self):

        global map_list
        global roads
        global sect
        global current_road

        current_road = map_list.popleft()



        if len(map_list) == 0:
            if sect == 0:
                map_list.extend(mapgenerate(start_map_graph,current_road,3))
            elif sect == 1:
                map_list.extend(mapgenerate(straight_map_graph,current_road,3))
            else:
                map_list.extend(mapgenerate(map_graph,current_road,3))
        
        
        
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

class Car(pygame.sprite.Sprite):

    def __init__(self, type, d):

        pygame.sprite.Sprite.__init__(self)

        self.d = d

        enemy = SpriteSheet("sprites/spritesheet.png")

        if d == "up":
            self.image = enemy.get_image(90, 0, 80, 100)
            self.rect = self.image.get_rect()
        elif d == "down":
            self.image = enemy.get_image(90, 100, 80, 100)
            self.rect = self.image.get_rect()

    def update(self):

        global scroll_speed

        if self.d == "up":
            self.rect.y -= scroll_speed*0.75
        elif self.d == "down":
            self.rect.y += scroll_speed

class Invis(pygame.sprite.Sprite):

    def __init__(self, width, height):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(KEY)
        self.rect = self.image.get_rect()

    def update(self):

        self.rect.y = 0

class MenuButton(pygame.sprite.Sprite):

    def __init__(self, text, type, action):

        pygame.sprite.Sprite.__init__(self)

        
        self.image = pygame.Surface([350, 80])
        self.rect = self.image.get_rect()
        
        self.type = type
        self.text = text
        self.action = action
        self.clicked = False

        pygame.font.init()
        self.font = pygame.font.Font("8-bit-hud.ttf", 25)
        self.updatesprite()
        
    def update(self):

        collides = self.rect.colliderect(mouse)
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if collides:
            self.type = 2
            if mouse_pressed and not self.clicked:
                self.clicked = True
                if self.action:
                    self.action()
            elif not mouse_pressed:
                self.clicked = False
        else:
            self.type = 1

        self.updatesprite()

    def updatesprite(self):

        button = SpriteSheet("sprites/spritesheet.png")

        if self.type == 1:
            self.image = button.get_image(170, 0, 350, 80)

        elif self.type == 2:
            self.image = button.get_image(170, 80, 350, 80)

        self.text_surface = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(self.text_surface, self.text_rect)


class MenuBackground(pygame.sprite.Sprite):

    def __init__(self, type):

        pygame.sprite.Sprite.__init__(self)

        background = SpriteSheet("sprites/menus/main_menu.png")

        if type == 1:
            self.image = background.get_image(0,0,1024,768)
            self.rect = self.image.get_rect()

class MouseObject(pygame.sprite.Sprite):

    def __init__(self):

        self.image = pygame.Surface([1, 1])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

class Logo(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        logo = SpriteSheet("sprites/spritesheet.png")

        self.image = logo.get_image(520, 0, 400, 240)
        self.rect = self.image.get_rect()

class Explosion(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        exp = SpriteSheet("sprites/spritesheet.png")

        self.image = exp.get_image(400, 160, 120, 120)
        self.rect = self.image.get_rect()

# screen definition

screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Action Fighter Game")

# map generation function

map_list = deque()
map_list.extend(mapgenerate(start_map_graph, "1m", 5))
current_road = map_list[0]

# print(map_list)

# sprite group definitions

all_sprites_list = pygame.sprite.Group()
all_backgrounds_list = pygame.sprite.Group()
all_players_list = pygame.sprite.Group()
all_roads_list = pygame.sprite.Group()
all_bullets_list = pygame.sprite.Group()
all_buttons_list = pygame.sprite.Group()
all_cars_list = pygame.sprite.Group()
all_enemies_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

# layer group definitions

# 1 = bottom, 10 = top

layer0_1 = pygame.sprite.Group() # background
layer0_2 = pygame.sprite.Group() # road
layer0_3 = pygame.sprite.Group()
layer0_4 = pygame.sprite.Group()
layer0_5 = pygame.sprite.Group() # bullets 
layer0_6 = pygame.sprite.Group() # player # enemies
layer0_7 = pygame.sprite.Group()
layer0_8 = pygame.sprite.Group()
layer0_9 = pygame.sprite.Group()
layer0_10 = pygame.sprite.Group() # invis

layer1_1 = pygame.sprite.Group() # background
layer1_2 = pygame.sprite.Group()
layer1_3 = pygame.sprite.Group() # buttons
layer1_4 = pygame.sprite.Group()

# sprite definitions

##player definition

player = Player(BLUE, 100, 100)
all_sprites_list.add(player)
all_players_list.add(player)
layer0_6.add(player)
player.rect.x = 472
player.rect.y = 534
player_list.add(player)

## background definition

background = Background()
all_sprites_list.add(background)
all_backgrounds_list.add(background)
layer0_1.add(background)
background.rect.x = 0
background.rect.y = 0

## road definition

road1 = Road(0)
# all_sprites_list.add(road)
# all_roads_list.add(road)
# layer0_2.add(road)
# road.rect.x = 0
# road.rect.y = 0
# road.y_float = 0
# road.num = 1
# road.gen()

road2 = Road(-768)
# all_sprites_list.add(road2)
# all_roads_list.add(road2)
# layer0_2.add(road2)
# road2.rect.x = 0
# road2.rect.y = -768
# road2.y_float = -768
# road2.num = 2
# road2.gen()

all_sprites_list.add(road1, road2)
all_roads_list.add(road1, road2)
layer0_2.add(road1, road2)

## enemy definition

# car1 = Car("car1", "up")
# all_sprites_list.add(car1)
# all_cars_list.add(car1)
# all_enemies_list.add(car1)
# layer0_6.add(car1)
# car1.rect.x = 512
# car1.rect.y = screen_height

## invis definition

invis = Invis(1024, 1)
all_sprites_list.add(invis)
# layer0_10.add(invis)
invis.rect.x = 0
invis.rect.y = 0

## button definitions

button1 = MenuButton("Play", 1, lambda: set_mode(0))
button1.rect.x = 337
button1.rect.y = 344
layer1_3.add(button1)
all_buttons_list.add(button1)

button2 = MenuButton("Settings", 1, lambda: set_mode(2))
button2.rect.x = 337
button2.rect.y = 444
layer1_3.add(button2)
all_buttons_list.add(button2)

## menu background definition

menubackground1 = MenuBackground(1)
menubackground1.rect.x = 0
menubackground1.rect.y = 0
layer1_1.add(menubackground1)

## mouse object definition

mouse = MouseObject()
mouse.rect.x = 0
mouse.rect.y = 0

## logo definition

logo = Logo()
logo.rect.x = 312
logo.rect.y = 84
layer1_4.add(logo)

## explosion testing

# explosion = Explosion()
# explosion.rect.x = 100
# explosion.rect.y = 100
# layer0_7.add(explosion)

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
            elif event.key == pygame.K_SPACE and distance > 10 and not dead:

                if player.bullets == 1:

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 35
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer0_5.add(bullet)

                elif player.bullets == 2:

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 60
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer0_5.add(bullet)

                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + 10
                    bullet.rect.y = player.rect.y
                    all_bullets_list.add(bullet)
                    all_sprites_list.add(bullet)
                    layer0_5.add(bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.W = False
            elif event.key == pygame.K_s:
                player.S = False
            elif event.key == pygame.K_a:
                player.A = False
            elif event.key == pygame.K_d:
                player.D = False

        elif event.type == explosion_timer:
            pygame.time.set_timer(explosion_timer, 0)
            print("quitting game")
            for sprite in layer0_10:
                if isinstance(sprite, Explosion):
                    sprite.kill()
            pygame.quit()
            exit()
            

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

    # invis mask

    invis_mask = pygame.mask.from_surface(invis.image)
    invis_mask_image = invis_mask.to_surface()
    invis_mask_image.set_colorkey(BLACK)
    
    # invis and road overlap

    ioverlap = invis_mask.overlap(road_mask, (road1.rect.x - invis.rect.x, road1.rect.y - invis.rect.y))
    ioverlap2 = invis_mask.overlap(road_mask2, (road2.rect.x - invis.rect.x, road2.rect.y - invis.rect.y))
    ioverlap_area = invis_mask.overlap_area(road_mask, (road1.rect.x - invis.rect.x, road1.rect.y - invis.rect.y))
    ioverlap2_area = invis_mask.overlap_area(road_mask2, (road2.rect.x - invis.rect.x, road2.rect.y - invis.rect.y))
    # if ioverlap:
    #     print(ioverlap[0], ioverlap[0] + ioverlap_area)
    # if ioverlap2:
    #     print(ioverlap2[0], ioverlap2[0] + ioverlap2_area)

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

    print(mode)

    if mode == 0:

        if not dead:
            player.update()

        background.update()

        for road in all_roads_list:
            road.update()

        for bullet in all_bullets_list:
            bullet.update()

        for car in all_cars_list:
            car.update()
            
        car_kill_list = pygame.sprite.groupcollide(all_bullets_list, all_cars_list, True, True)

        car_hit_list = pygame.sprite.groupcollide(all_cars_list, player_list, False, False)

        if dead == True:
            scroll_speed = 0
        elif scroll_speed < max_speed:
            scroll_speed = round(scroll_speed + 0.05, 3)

        if car_hit_list:
            scroll_speed = 0
            exp = Explosion()
            exp.rect.center = ((car.rect.centerx + player.rect.centerx) // 2, (car.rect.centery + player.rect.centery) // 2)
            layer0_10.add(exp)
            player.yspeed = 0
            player.xspeed = 0
            dead = True
            pygame.time.set_timer(explosion_timer, 1000)
            print("timer started")
            
        for car in car_hit_list:
            car.kill()

        invis.update()

        # invisible mouse

        pygame.mouse.set_visible(False)

        sect_check()

        car_timer += 1

        print(current_road)

        if sect == 1 and current_road == "1m":
            car_gen()

    if mode == 1:

        pygame.mouse.set_visible(True)

        mouse.rect.x, mouse.rect.y = pygame.mouse.get_pos()

        for button in all_buttons_list:
            button.update()

    #print(scroll_speed)

    #print(road.rect.y, road.rect.x)
    #print(road2.rect.y, road2.rect.x)

    # screen drawing

    screen.fill(BLACK)

    if mode == 0:
        layer0_1.draw(screen)
        layer0_2.draw(screen)
        layer0_3.draw(screen)
        layer0_4.draw(screen)
        layer0_5.draw(screen)
        layer0_6.draw(screen)
        layer0_7.draw(screen)
        layer0_8.draw(screen)
        layer0_9.draw(screen)
        layer0_10.draw(screen)
    if mode == 1:
        layer1_1.draw(screen)
        layer1_2.draw(screen)
        layer1_3.draw(screen)
        layer1_4.draw(screen)

    # screen.blit(combined_road_mask_image, (0,0))
    # screen.blit(player_mask_image, (0, 0))
    # screen.blit(road_mask_image, road1.rect.topleft)
    # screen.blit(road_mask_image2, road2.rect.topleft)
    # screen.blit(background_mask_image, (0,0))
    # screen.blit(invis_mask_image, (0,0))


    # screen update

    clock.tick(60)

    pygame.display.flip()

pygame.quit()