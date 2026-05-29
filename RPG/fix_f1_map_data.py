import re

W, H = 80, 80
lines = [['1' for _ in range(W)] for _ in range(H)]

def draw_room(cx, cy, w, h, tile='0'):
    for y in range(cy-h//2, cy+h//2):
        for x in range(cx-w//2, cx+w//2):
            if 0 <= y < H and 0 <= x < W:
                lines[y][x] = tile

# [1] 転移門 (40, 75)
draw_room(40, 75, 10, 8)
lines[76][40] = 'c'

# 通路: 転移門 -> 迎賓の回廊
draw_room(40, 65, 4, 15)

# [2] 迎賓の回廊 (40, 55)
draw_room(40, 55, 12, 10)

# [4] 秘密の備蓄庫 (東側)
draw_room(52, 55, 6, 6)

# 通路: 迎賓の回廊 -> HUB
draw_room(40, 45, 4, 15)

# [3] 中央大広間 (HUB) (40, 35)
draw_room(40, 35, 16, 12) # y=29~40, x=32~47

# HUB北側に壁を作り、中央の通路(x=38~41)を青扉(4)で塞ぐ
for x in range(32, 48):
    lines[29][x] = '1'
lines[29][38] = '4'
lines[29][39] = '4'
lines[29][40] = '4'
lines[29][41] = '4'

# [15] 審判の交差点 (40, 20)
draw_room(40, 20, 10, 8) # y=16~23, x=35~44
# 交差点からHUBへの合流 (y=23~29)
draw_room(40, 26, 4, 6)  # y=23~28, x=38~41

# HUBから東への通路
draw_room(55, 35, 15, 4) # x=47~62, y=33~36
# 緑扉で塞ぐ
for y in range(33, 37):
    lines[y][50] = '8'

# [7] 閉ざされた書庫 (65, 35)
draw_room(65, 35, 10, 10)

# [6] 蜘蛛の巣穴（中ボス） (70, 20)
draw_room(70, 20, 14, 14)
# 書庫から中ボスへの連絡橋
draw_room(68, 28, 4, 10)

# [5] 東の居住区 / 連絡通路 (55, 20)
draw_room(55, 20, 8, 8)
draw_room(60, 20, 10, 4)

# 居住区から審判の交差点への一方通行
draw_room(48, 20, 10, 4)

# HUBから西への通路
draw_room(25, 35, 15, 4)

# [11] 崩れた西棟 (20, 35)
draw_room(15, 35, 12, 12)

# [12] 処刑人の間(罠部屋) (15, 20)
draw_room(15, 20, 12, 12)
draw_room(15, 28, 4, 8)

# [13] 遺骸の安置所(西の瞳) (15, 10)
draw_room(15, 10, 10, 8)
draw_room(15, 15, 4, 6)

# 安置所から交差点への通路
draw_room(28, 10, 20, 4)
draw_room(40, 13, 4, 6)

# [16] 守護者の間 (BOSS) (40, 8)
draw_room(40, 8, 20, 14)
# ボス部屋手前の通路
draw_room(40, 17, 6, 6)

# [14] 崩落した抜け道（ショトカ）
draw_room(25, 45, 6, 20)
draw_room(32, 55, 10, 4)
# 紫扉（ショトカ鍵）
for y in range(53, 57):
    lines[y][30] = '9'

out = "tiles: [\n"
for r in lines:
    out += '    "' + ''.join(r) + '",\n'
out += "],\n"

out += "portals: [{ c: 40, r: 76, dest: 'city', sc: 75, sr: 30 }],\n"
out += "npcs: [],\n"
out += "enemies: [\n"
out += "    { c: 39, r: 54, type: 'slime' }, { c: 41, r: 56, type: 'slime' },\n"
out += "    { c: 50, r: 55, type: 'slime' },\n"
out += "    { c: 70, r: 20, type: 'mini_boss' },\n"
out += "    { c: 13, r: 19, type: 'bat' }, { c: 17, r: 21, type: 'bat' }, { c: 15, r: 20, type: 'bat' },\n"
out += "    { c: 68, r: 30, type: 'skeleton' }, { c: 66, r: 32, type: 'skeleton' },\n"
out += "    { c: 40, r: 8, type: 'boss' }\n"
out += "],\n"
out += "chests: [\n"
out += "    { c: 54, r: 55, opened: false, keyId: 'gold', color: '#fbbf24' },\n"
out += "    { c: 15, r: 10, opened: false, keyId: 'start', color: '#38bdf8' },\n" # 西の瞳
out += "    { c: 72, r: 18, opened: false, keyId: 'forest', color: '#10b981' },\n" # 東の瞳
out += "    { c: 15, r: 35, opened: false, keyId: 'crystal', color: '#9d4edd' },\n" # 紫の鍵を追加(西棟)
out += "]"

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 置換する部分を正確に特定
pattern = r"tiles:\s*\[[\s\S]*?\],\s*portals:[\s\S]*?chests:\s*\[[\s\S]*?\],"
replacement = out + ","

new_content = re.sub(pattern, replacement, content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Map updated successfully.")
