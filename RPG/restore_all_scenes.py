import re

# 1. city_tiles 生成 (generate_city.pyと同じ)
W, H = 80, 60
cx, cy = 40, 30
R = 25
city_lines = []
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
    city_lines.append(list(row))

city_lines[cy][cx] = '5'
city_lines[cy-1][cx] = '1'
city_lines[cy+1][cx] = '1'
city_lines[cy][cx-1] = '1'
city_lines[cy][cx+1] = '1'

# ギルド、その他の建物
city_lines[cy-15][cx] = 'i' 
city_lines[cy-10][cx-15] = 'd'
city_lines[cy+10][cx-15] = 'g'
city_lines[cy+5][cx-10] = 'e'
city_lines[cy+5][cx+15] = 'j'
city_lines[cy+15][cx] = 'f'

for x in range(cx+25, cx+36):
    city_lines[cy][x] = '0'
    city_lines[cy-1][x] = '1'
    city_lines[cy+1][x] = '1'
city_lines[cy][cx+35] = 'c'

for x in range(cx-36, cx-25):
    city_lines[cy][x] = '0'
    city_lines[cy-1][x] = '1'
    city_lines[cy+1][x] = '1'

city_tiles_str = "[\n"
for l in city_lines:
    city_tiles_str += '                    "' + ''.join(l) + '",\n'
city_tiles_str += "                ]"

city_def = f"""
            'city': {{
                width: 80, height: 60,
                tiles: {city_tiles_str},
                portals: [
                    {{ c: 40, r: 15, dest: 'guild', sc: 10, sr: 13 }},
                    {{ c: 75, r: 30, dest: 'dungeon_f1', sc: 40, sr: 75 }}
                ],
                npcs: [
                    {{ c: 40, r: 28, id: 'guide', name: "街の案内人" }}
                ],
                enemies: [], chests: [],
                getTheme: () => themes.city
            }}"""

# 2. guild_def 生成
guild_def = """
            'guild': {
                width: 20, height: 15,
                tiles: [
                    "11111111111111111111",
                    "10000000000000000001",
                    "10000111100111100001",
                    "10000100000000100001",
                    "10000100060000100001",
                    "10000111100111100001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000005000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "11111111111211111111"
                ],
                portals: [
                    { c: 10, r: 14, dest: 'city', sc: 40, sr: 16 }
                ],
                npcs: [
                    { c: 9, r: 4, id: 'guildmaster', name: "ギルドマスター" }
                ],
                enemies: [], chests: [],
                getTheme: () => themes.guild
            }"""

# 3. dungeon_f1 生成
W, H = 80, 80
f1_lines = [['1' for _ in range(W)] for _ in range(H)]

def draw_room(cx, cy, w, h, tile='0'):
    for y in range(cy-h//2, cy+h//2):
        for x in range(cx-w//2, cx+w//2):
            if 0 <= y < H and 0 <= x < W:
                f1_lines[y][x] = tile

draw_room(40, 75, 10, 8)
f1_lines[76][40] = 'c'
draw_room(40, 65, 4, 15)
draw_room(40, 55, 12, 10)
draw_room(52, 55, 6, 6)
draw_room(40, 45, 4, 15)
draw_room(40, 35, 16, 12)
for x in range(32, 48):
    f1_lines[29][x] = '1'
f1_lines[29][38] = '4'
f1_lines[29][39] = '4'
f1_lines[29][40] = '4'
f1_lines[29][41] = '4'
draw_room(40, 20, 10, 8)
draw_room(40, 26, 4, 6)
draw_room(55, 35, 15, 4)
for y in range(33, 37):
    f1_lines[y][50] = '8'
draw_room(65, 35, 10, 10)
draw_room(70, 20, 14, 14)
draw_room(68, 28, 4, 10)
draw_room(55, 20, 8, 8)
draw_room(60, 20, 10, 4)
draw_room(48, 20, 10, 4)
draw_room(25, 35, 15, 4)
draw_room(15, 35, 12, 12)
draw_room(15, 20, 12, 12)
draw_room(15, 28, 4, 8)
draw_room(15, 10, 10, 8)
draw_room(15, 15, 4, 6)
draw_room(28, 10, 20, 4)
draw_room(40, 13, 4, 6)
draw_room(40, 8, 20, 14)
draw_room(40, 17, 6, 6)
draw_room(25, 45, 6, 20)
draw_room(32, 55, 10, 4)
for y in range(53, 57):
    f1_lines[y][30] = '9'

f1_tiles_str = "[\n"
for l in f1_lines:
    f1_tiles_str += '                    "' + ''.join(l) + '",\n'
f1_tiles_str += "                ]"

dungeon_f1_def = f"""
            'dungeon_f1': {{
                width: 80, height: 80,
                tiles: {f1_tiles_str},
                portals: [
                    {{ c: 40, r: 76, dest: 'city', sc: 74, sr: 30 }}
                ],
                npcs: [],
                enemies: [
                    {{ c: 39, r: 54, type: 'slime' }}, {{ c: 41, r: 56, type: 'slime' }},
                    {{ c: 50, r: 55, type: 'slime' }},
                    {{ c: 70, r: 20, type: 'mini_boss' }},
                    {{ c: 13, r: 19, type: 'bat' }}, {{ c: 17, r: 21, type: 'bat' }}, {{ c: 15, r: 20, type: 'bat' }},
                    {{ c: 68, r: 30, type: 'skeleton' }}, {{ c: 66, r: 32, type: 'skeleton' }},
                    {{ c: 40, r: 8, type: 'boss' }}
                ],
                chests: [
                    {{ c: 54, r: 55, opened: false, keyId: 'gold', color: '#fbbf24' }},
                    {{ c: 15, r: 10, opened: false, keyId: 'start', color: '#38bdf8' }},
                    {{ c: 72, r: 18, opened: false, keyId: 'forest', color: '#10b981' }},
                    {{ c: 15, r: 35, opened: false, keyId: 'crystal', color: '#9d4edd' }}
                ],
                getTheme: () => themes.dungeon
            }}"""

dungeon_f2_def = """
            'dungeon_f2': {
                width: 40, height: 40,
                tiles: Array(40).fill("1".repeat(40)),
                portals: [{ c: 20, r: 38, dest: 'dungeon_f1', sc: 40, r: 8 }],
                npcs: [], enemies: [], chests: [],
                getTheme: () => themes.crystal
            }"""

new_sceneData = f"const sceneData = {{{city_def},{guild_def},{dungeon_f1_def},{dungeon_f2_def}\n        }};"

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 置換
# "const sceneData = {" から、次に let MAP_COLS が出てくる直前までを置換
pattern = r"const sceneData = \{[\s\S]*?(?=// ====== エンティティ定義とマップロードシステム ======)"
new_content = re.sub(pattern, new_sceneData + "\n\n        ", content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Restored all scenes successfully.")
