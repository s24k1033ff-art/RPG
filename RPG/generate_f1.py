W, H = 80, 80
lines = [['1' for _ in range(W)] for _ in range(H)]

def draw_room(cx, cy, w, h, tile='0'):
    for y in range(cy-h//2, cy+h//2):
        for x in range(cx-w//2, cx+w//2):
            if 0 <= y < H and 0 <= x < W:
                lines[y][x] = tile

# [1] 転移門 (40, 75)
draw_room(40, 75, 10, 8)
lines[76][40] = 'c' # 街へのポータル

# 通路: 転移門 -> 迎賓の回廊
draw_room(40, 65, 4, 15)

# [2] 迎賓の回廊 (40, 55)
draw_room(40, 55, 12, 10)

# [4] 秘密の備蓄庫 (東側)
draw_room(52, 55, 6, 6) # 隠し部屋

# 通路: 迎賓の回廊 -> HUB
draw_room(40, 45, 4, 15)

# [3] 中央大広間 (HUB) (40, 35)
draw_room(40, 35, 16, 12)
lines[30][39] = '4' # 青扉（鍵）
lines[30][40] = '4'
lines[30][41] = '4'

# 通路: HUB -> 東西
draw_room(25, 35, 15, 4) # 西へ
draw_room(55, 35, 15, 4) # 東へ (閉ざされた書庫手前)
lines[34][50] = '8' # 緑扉（錆びた鍵相当）
lines[35][50] = '8'

# [7] 閉ざされた書庫 (65, 35)
draw_room(65, 35, 10, 10)

# [6] 蜘蛛の巣穴（中ボス） (70, 20)
draw_room(70, 20, 14, 14)
# 書庫から中ボスへの連絡橋
draw_room(68, 28, 4, 10)

# [5] 東の居住区 / 連絡通路 (55, 20)
draw_room(55, 20, 8, 8)
draw_room(60, 20, 10, 4) # 中ボスから居住区

# 居住区から審判の交差点への一方通行（段差=穴など）
draw_room(48, 20, 10, 4)

# [15] 審判の交差点 (40, 20)
draw_room(40, 20, 10, 8)
# 交差点からHUBへの合流
draw_room(40, 26, 4, 6) 

# [11] 崩れた西棟 (20, 35)
draw_room(15, 35, 12, 12)

# [12] 処刑人の間(罠部屋) (15, 20)
draw_room(15, 20, 12, 12)
draw_room(15, 28, 4, 8) # 西棟から罠部屋へ

# [13] 遺骸の安置所(西の瞳) (15, 10)
draw_room(15, 10, 10, 8)
draw_room(15, 15, 4, 6) # 罠部屋から安置所へ

# 安置所から交差点への通路
draw_room(28, 10, 20, 4)
draw_room(40, 13, 4, 6)

# [16] 守護者の間 (BOSS) (40, 8)
draw_room(40, 8, 20, 14)
# ボス部屋手前の通路
draw_room(40, 17, 6, 6)

# [14] 崩落した抜け道（ショトカ）
draw_room(25, 45, 6, 20)
draw_room(32, 55, 10, 4) # 回廊へ
lines[54][30] = '9' # 紫扉（ショトカ鍵）
lines[55][30] = '9'

out = "tiles: [\n"
for r in lines:
    out += '    "' + ''.join(r) + '",\n'
out += "],\n"

# JSON or JS object 構成
out += "portals: [{ c: 40, r: 76, dest: 'city', sc: 75, sr: 30 }],\n"
out += "npcs: [],\n"
out += "enemies: [\n"
out += "    { c: 39, r: 54, type: 'slime' }, { c: 41, r: 56, type: 'slime' },\n" # チュートリアル
out += "    { c: 50, r: 55, type: 'slime' },\n" # 隠し部屋前
out += "    { c: 70, r: 20, type: 'boss' },\n" # 中ボス(ウィーバーの代用)
out += "    { c: 13, r: 19, type: 'bat' }, { c: 17, r: 21, type: 'bat' }, { c: 15, r: 20, type: 'bat' },\n" # 罠部屋コウモリ
out += "    { c: 68, r: 30, type: 'skeleton' }, { c: 66, r: 32, type: 'skeleton' },\n" # 連絡橋
out += "    { c: 40, r: 8, type: 'boss' }\n" # 大ボス
out += "],\n"
out += "chests: [\n"
out += "    { c: 54, r: 55, opened: false, keyId: 'gold', color: '#fbbf24' },\n" # 隠し部屋
out += "    { c: 15, r: 10, opened: false, keyId: 'start', color: '#38bdf8' },\n" # 西の瞳(青扉キー)
out += "    { c: 72, r: 18, opened: false, keyId: 'forest', color: '#10b981' },\n" # 東の瞳＋錆びた鍵(緑扉キー)
out += "]"

with open('map_out.txt', 'w', encoding='utf-8') as f:
    f.write(out)
