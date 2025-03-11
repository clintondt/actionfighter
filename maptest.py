import mapgen as module
from mapgen import map_graph
import random

inp = str(input())

arr = []

x = 0

def next(inp):

    if inp not in map_graph:
        print(f"Error: {inp} not found in map_graph")
        return inp

    res = map_graph.get(inp)

    # print(res)

    length = len(res)

    pick = random.randint(0, length-1)

    inp = str(map_graph.get(inp)[pick])

    return inp

while x <= 100:
    inp = next(inp)
    arr.append(inp)
    x += 1

# print(len(map_graph.get(inp)))

print(arr)