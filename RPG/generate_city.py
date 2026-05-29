W, H = 80, 60
cx, cy = 40, 30
R = 25

lines = []
for y in range(H):
    row = ''
    for x in range(W):
        dist = ((x - cx)**2 + (y - cy)**2)**0.5
        if dist > R + 1:
            row += '2'
        elif dist > R:
            row += '1'
        else:
            row += '0'
    lines.append(list(row))

lines[cy][cx] = '5'
lines[cy-1][cx] = '1'
lines[cy+1][cx] = '1'
lines[cy][cx-1] = '1'
lines[cy][cx+1] = '1'

lines[cy-15][cx] = 'i' 
lines[cy-10][cx-15] = 'd'
lines[cy+10][cx-15] = 'g'
lines[cy+5][cx-10] = 'e'
lines[cy+5][cx+15] = 'j'
lines[cy+15][cx] = 'f'

for x in range(cx+25, cx+36):
    lines[cy][x] = '0'
    lines[cy-1][x] = '1'
    lines[cy+1][x] = '1'
lines[cy][cx+35] = 'c'

for x in range(cx-36, cx-25):
    lines[cy][x] = '0'
    lines[cy-1][x] = '1'
    lines[cy+1][x] = '1'

out = '                tiles: [\n'
for l in lines:
    out += '                    "' + ''.join(l) + '",\n'
out += '                ],'
with open('map_out.txt', 'w') as f:
    f.write(out)
