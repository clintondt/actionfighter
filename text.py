import pprint

inp = int(input())
inp = str(inp)

alist = []
tlist = []

for x in range(len(inp)):
    if x % 2 == 0:
        alist.append(inp[x])
    else:
        tlist.append(inp[x])

salist = sorted(alist)
stlist = sorted(tlist)
galist = int(salist[-1])
gtlist = int(stlist[-1])

totalt = 0
for x in range(len(tlist)):
    totalt += int(tlist[x])
#print(totalt)

wave = [["."]*totalt for _ in range(10)]

currt = 0

for x in range(len(alist)):
    a = int(alist[x])
    t = int(tlist[x])
    for y in range(t):
        wave[galist + 2-a][currt] = "@"
        currt += 1

#print(galist, gtlist)

wavestr = ""

for x in range(len(wave)):
    for y in range(len(wave[x])):
        if y == len(wave[x])-1:
            wavestr += wave[x][y] + "\n"
        else:
            wavestr += wave[x][y]
    
pprint.pprint(wave)

