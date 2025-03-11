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