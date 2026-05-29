import re

W, H = 80, 60
cx, cy = 40, 30
R = 25

lines = []
for y in range(H):
    row = []
    for x in range(W):
        dist = ((x - cx)**2 + (y - cy)**2)**0.5
        if dist > R + 1:
            row.append('2')
        elif dist > R:
            row.append('1')
        else:
            row.append('0')
    lines.append(row)

lines[cy][cx] = '5'
lines[cy-1][cx] = '1'
lines[cy+1][cx] = '1'
lines[cy][cx-1] = '1'
lines[cy][cx+1] = '1'

def draw_building(bx, by, w, h, door):
    for y in range(by - h, by + 1):
        for x in range(bx - w, bx + w + 1):
            if 0 <= x < W and 0 <= y < H and lines[y][x] == '0':
                lines[y][x] = 'a'
    lines[by][bx] = door

draw_building(cx, cy-15, 3, 4, 'i') # 領主邸
draw_building(cx-15, cy-10, 2, 3, 'd') # ギルド
draw_building(cx-15, cy+10, 2, 3, 'g') # 宿屋
draw_building(cx-10, cy+5, 2, 2, 'e') # 鍛冶屋
draw_building(cx+15, cy+5, 2, 3, 'j') # 暗殺者
draw_building(cx, cy+15, 2, 2, 'f') # 魔法屋

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

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"('city':\s*\{\s*width:\s*80,\s*height:\s*60,[^{}]*?)\s*tiles:\s*\[[\s\S]*?\],"
new_content = re.sub(pattern, r'\1' + '\n' + out, content)

# 戻り先ポータルの修正
new_content = new_content.replace("{ c: 10, r: 14, dest: 'city', sc: 20, sr: 25 }", "{ c: 10, r: 14, dest: 'city', sc: 30, sr: 36 }")
new_content = new_content.replace("{ c: 10, r: 14, dest: 'city', sc: 10, sr: 25 }", "{ c: 10, r: 14, dest: 'city', sc: 25, sr: 21 }")
new_content = new_content.replace("{ c: 10, r: 14, dest: 'city', sc: 10, sr: 13 }", "{ c: 10, r: 14, dest: 'city', sc: 25, sr: 21 }")

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done!')
