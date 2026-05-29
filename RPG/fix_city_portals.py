import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 街のポータルデータを完全に修正する
old_portals = r"'city': \{[\s\S]*?portals: \[([\s\S]*?)\]"
# cityのportalsの中身だけを置換する
city_pattern = r"('city': \{[\s\S]*?portals: \[)([\s\S]*?)(\])"
new_city_portals = r"""\1
                    { c: 25, r: 20, dest: 'guild', sc: 9, sr: 9 }, // ギルド 'd'
                    { c: 75, r: 30, dest: 'dungeon_f1', sc: 40, sr: 74 } // ダンジョン 'c'
                \3"""
c = re.sub(city_pattern, new_city_portals, c)

# 2. 建物の枠が表示されない問題の修正
# 実は tile === 1 の時に fillColor が設定されていなかったり、透明になっていたりする可能性がある。
# もう一度レンダリング処理をきれいに上書きする
old_render = r"if \(tile === 'a'\) \{ ctx\.fillStyle = '#1e3a8a'; \} // コンベア\s*else if \(tile === 'v'\) \{ ctx\.fillStyle = '#166534'; \} // ツタ\s*else if \(tile === 1\) \{ ctx\.fillStyle = theme\.wall; ctx\.fillRect\(tx, ty, TILE_SIZE, TILE_SIZE\); ctx\.strokeStyle = theme\.border; ctx\.lineWidth = 1; ctx\.strokeRect\(tx, ty, TILE_SIZE, TILE_SIZE\); \}"

new_render = """if (tile === 'a') { ctx.fillStyle = '#1e3a8a'; ctx.fillRect(tx, ty, TILE_SIZE, TILE_SIZE); } // コンベア
                    else if (tile === 'v') { ctx.fillStyle = '#166534'; ctx.fillRect(tx, ty, TILE_SIZE, TILE_SIZE); } // ツタ
                    else if (tile === 1 || tile === '1') { ctx.fillStyle = theme.wall; ctx.fillRect(tx, ty, TILE_SIZE, TILE_SIZE); ctx.strokeStyle = theme.border; ctx.lineWidth = 1; ctx.strokeRect(tx, ty, TILE_SIZE, TILE_SIZE); }"""
c = re.sub(old_render, new_render, c)

# parseIntの修正がどうなっているか再確認し、確実に文字の '1' や数値の 1 をキャッチできるように '1' の条件を render に足した (tile === 1 || tile === '1')

# 3. ギルドと鍛冶屋に入れない問題
# triggerInteract() のショップや鍛冶屋の判定がどうなっているか
# 鍛冶屋はまだ施設がないが、ショップ(5)と調理鍋(16)は直接判定している。
# ギルドはポータル(13, 'd')として入る。街のタイルで 'd' (13), 'e' (14), 'f' (15) となっている。
# 現在 parseInt(char, 36) なので 'd' は 13。
# update() でのポータル判定は: currentTile >= 12 && currentTile <= 16
# これなら guild (13) や dungeon (12) に乗ったときにポータルワープ処理が走る。

# c を書き戻す
with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied city portals and fixed render bug!")
