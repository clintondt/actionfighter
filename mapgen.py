import pygame
import math
import random
import time
from collections import deque

map_graph = {

    # 1 to x
    
    "1m": ["1m", "1ml", "1mr", "1m2lm", "1m2lr", "1m2rm"],
    "1l": ["1l", "1lm", "1l2lm"],
    "1r": ["1r", "1rm", "1r2rm"],
    "1ml": ["1l"],
    "1mr": ["1r"],
    "1lm": ["1m", "1mr"],
    "1rm": ["1m", "1ml"],

    # 2 to x

    "2lm": ["2lm", "2lm2rm", "2lm1l", "2lm1m"],
    "2lr": ["2lr", "2lr2rm", "2lr2lm", "2lr1l", "2lr1r"],
    "2rm": ["2rm", "2rm2lm", "2rm1r", "2rm1m"],
    "1m2lm": ["2lm"],
    "1m2lr": ["2lr"],
    "1m2rm": ["2rm"],
    "1l2lm": ["2lm"],
    "1r2rm": ["2rm"],
    "2lm2rm": ["2rm"],
    "2lr2rm": ["2rm"],
    "2lr2lm": ["2lm"],
    "2rm2lm": ["2lm"],
    "2lr1l": ["1l"],
    "2lr1r": ["1r"],
    "2lm1m": ["1m"],
    "2lm1l": ["1l"],
    "2rm1m": ["1m"],
    "2rm1r": ["1r"]

}

road_images = {

    "1m": "sprites/roads/1m.png",
    "1l": "sprites/roads/1l.png", 
    "1r": "sprites/roads/1r.png",
    "1ml": "sprites/roads/1ml.png",
    "1mr": "sprites/roads/1mr.png",
    "1lm": "sprites/roads/1lm.png",
    "1rm": "sprites/roads/1rm.png",
    "2lm": "sprites/roads/2lm.png",
    "2lr": "sprites/roads/2lr.png",
    "2rm": "sprites/roads/2rm.png",
    "1m2lm": "sprites/roads/1m2lm.png",
    "1m2lr": "sprites/roads/1m2lr.png",
    "1m2rm": "sprites/roads/1m2rm.png",
    "1l2lm": "sprites/roads/1l2lm.png",
    "1r2rm": "sprites/roads/1r2rm.png",
    "2lm2rm": "sprites/roads/2lm2rm.png",
    "2lr2rm": "sprites/roads/2lr2rm.png",
    "2lr2lm": "sprites/roads/2lr2lm.png",
    "2rm2lm": "sprites/roads/2rm2lm.png",
    "2lr1l": "sprites/roads/2lr1l.png",
    "2lr1r": "sprites/roads/2lr1r.png",
    "2lm1m": "sprites/roads/2lm1m.png",
    "2lm1l": "sprites/roads/2lm1l.png",
    "2rm1m": "sprites/roads/2rm1m.png",
    "2rm1r": "sprites/roads/2rm1r.png"
}

__all__ = ['road_images']