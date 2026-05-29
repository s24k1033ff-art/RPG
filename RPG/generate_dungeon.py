import re
import random

def generate_dungeon_map():
    width = 80
    height = 80
    
    # 全部壁で初期化
    tiles = [["1" for _ in range(width)] for _ in range(height)]
    
    def fill_rect(x, y, w, h, char):
        for r in range(y, y+h):
            for c in range(x, x+w):
                if 0 <= r < height and 0 <= c < width:
                    tiles[r][c] = char

    # 1. 北のスタート地点（ポータル）
    fill_rect(35, 1, 10, 8, "0")
    tiles[2][40] = "c" # 出口ポータル
    
    # 2. メイン通路 (縦)
    fill_rect(38, 9, 4, 50, "0")
    
    # 3. 各所に部屋を生成
    rooms = []
    for _ in range(15):
        w = random.randint(8, 16)
        h = random.randint(8, 16)
        x = random.randint(5, width - w - 5)
        y = random.randint(10, 50)
        fill_rect(x, y, w, h, "0")
        rooms.append((x, y, w, h))
        # メイン通路へ向かって横の通路を掘る
        if x < 40:
            fill_rect(x + w, y + h//2, 40 - (x + w), 2, "0")
        else:
            fill_rect(40, y + h//2, x - 40, 2, "0")
            
    # 4. 罠部屋や穴を追加
    for rx, ry, rw, rh in rooms[:5]:
        fill_rect(rx+2, ry+2, rw-4, rh-4, "2") # 穴
        fill_rect(rx+3, ry+3, rw-6, rh-6, "0") # 穴の中の浮島
    for rx, ry, rw, rh in rooms[5:10]:
        fill_rect(rx+2, ry+2, rw-4, rh-4, "3") # トゲ罠
        fill_rect(rx+3, ry+3, rw-6, rh-6, "0")
        
    # 5. ボス部屋 (最深部)
    fill_rect(20, 60, 40, 18, "0")
    fill_rect(38, 59, 4, 1, "0") # ボス部屋への入り口を開通
    
    # 文字列変換
    str_tiles = ["".join(row) for row in tiles]
    
    # enemies の大量配置
    enemies_str = "[\n"
    for rx, ry, rw, rh in rooms:
        # 部屋ごとに数匹
        num = random.randint(2, 4)
        for _ in range(num):
            ex = random.randint(rx+1, rx+rw-2)
            ey = random.randint(ry+1, ry+rh-2)
            etype = random.choice(['slime', 'slime', 'wind_slime', 'guardian'])
            enemies_str += f"                    {{c: {ex}, r: {ey}, type: '{etype}'}},\n"
    # ボス追加
    enemies_str += f"                    {{c: 40, r: 70, type: 'boss'}}\n                ]"
    
    # インデント付きのJS配列形式
    js_array = "[\n"
    for row in str_tiles:
        js_array += f'                    "{row}",\n'
    js_array += "                ]"
    
    return js_array, enemies_str

js_array, enemies_str = generate_dungeon_map()

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# dungeon_f1 の置換
start_idx = content.find("'dungeon_f1': {")
if start_idx != -1:
    width_start = content.find("width:", start_idx)
    width_end = content.find(",", width_start)
    content = content[:width_start] + "width: 80, height: 80" + content[width_end+12:] # 既存の width, height を削除して入れ替え
    
    tiles_start = content.find("tiles: [", start_idx)
    tiles_end = content.find("],", tiles_start) + 1
    content = content[:tiles_start] + "tiles: " + js_array + content[tiles_end:]
    
    enemies_start = content.find("enemies: [", start_idx)
    enemies_end = content.find("],", enemies_start) + 1
    content = content[:enemies_start] + "enemies: " + enemies_str + content[enemies_end:]

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Dungeon expanded!")
