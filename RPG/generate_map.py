import re

def generate_city_map():
    width = 80
    height = 60
    
    # 基本はすべて壁(1)で初期化
    tiles = [["1" for _ in range(width)] for _ in range(height)]
    
    def fill_rect(x, y, w, h, char):
        for r in range(y, y+h):
            for c in range(x, x+w):
                if 0 <= r < height and 0 <= c < width:
                    tiles[r][c] = char

    # 全体をくりぬいて床(0)にする (境界1マスは壁)
    fill_rect(1, 1, width-2, height-2, "0")
    
    # 中央の広場 (噴水や碑石を置く)
    # 中心は (40, 30)
    
    # 北の貴族街 (領主邸など)
    fill_rect(1, 1, width-2, 15, "0")
    fill_rect(10, 5, 20, 8, "1") # 領主邸の壁
    tiles[12][20] = "i" # i: 領主邸のドア (新設)
    
    # 西の商業区画 (ギルド、鍛冶屋など)
    fill_rect(5, 20, 20, 5, "1") # ギルドと鍛冶屋の建物
    tiles[24][10] = "d" # d: ギルドドア
    tiles[24][20] = "e" # e: 鍛冶屋ドア
    
    # 東の居住区・商業区 (魔法屋、宿屋など)
    fill_rect(55, 20, 20, 5, "1")
    tiles[24][60] = "f" # f: 魔法屋ドア
    tiles[24][70] = "g" # g: 宿屋ドア
    
    # 中央広場
    fill_rect(35, 28, 10, 4, "0")
    tiles[30][40] = "5" # 5: 碑石
    
    # 南のアビス・ゲート周辺 (ダンジョンポータル)
    # スラム街や怪しい裏通り
    fill_rect(15, 45, 10, 5, "1") # 暗殺者ギルド等
    tiles[45][20] = "j" # j: 暗殺者ギルドドア (新設)
    
    # ダンジョンポータル (南端)
    fill_rect(35, 50, 10, 8, "0")
    tiles[55][40] = "c" # c: ダンジョンポータル
    
    # リストを文字列のリストに変換
    str_tiles = ["".join(row) for row in tiles]
    
    # インデント付きのJS配列形式にフォーマット
    js_array = "[\n"
    for row in str_tiles:
        js_array += f'                    "{row}",\n'
    js_array += "                ]"
    return js_array

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 正規表現で city の tiles 部分を置換
pattern = re.compile(r"('city':\s*\{\s*width:\s*\d+,\s*height:\s*\d+.*?tiles:\s*\[\s*).*?(\s*\],\s*portals:)", re.DOTALL)

new_tiles = generate_city_map()

# width, height も書き換える
content = re.sub(r"('city':\s*\{\s*width:)\s*\d+,\s*height:\s*\d+", r"\g<1> 80, height: 60", content)

# tiles 配列の置き換え
# 置換用関数を使う
def replacer(match):
    return match.group(1) + "\n" + "\n".join(['                    "' + "".join(row) + '",' for row in [list(r) for r in new_tiles.strip()[2:-2].split('",\n')]]) + "\n                " + match.group(2)

# 新しいマップを挿入 (簡易的な置換)
# 一旦、tiles部分を直接文字列操作で差し替える
start_str = "'city': {"
start_idx = content.find(start_str)
if start_idx != -1:
    tiles_start = content.find("tiles: [", start_idx)
    tiles_end = content.find("],", tiles_start) + 1
    
    new_content = content[:tiles_start] + "tiles: " + new_tiles + content[tiles_end:]
    
    # プレイヤーの初期位置やポータルの位置も変更する必要がある
    # ここではPythonを使って一気に書き換えてしまう。
    
    with open('preview_demo.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Map generated and updated successfully.")
else:
    print("Could not find city map in preview_demo.html")
