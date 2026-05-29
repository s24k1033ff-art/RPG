import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. useSkill に間違って入ったハザード処理を取り除く
bad_use_skill = """let dx = 0, dy = 0; if (keys['w']) dy = -1; if (keys['s']) dy = 1; if (keys['a']) dx = -1; if (keys['d']) dx = 1;
            
            // 環境ハザード: コンベア床 (a) と ツタ (v)
            const pTile = getTileAt(player.x, player.y);
            if (pTile === 'a') {
                // コンベアは下向き(南)へ流すとする
                player.y += 150 * dt;
            }"""
good_use_skill = "let dx = 0, dy = 0; if (keys['w']) dy = -1; if (keys['s']) dy = 1; if (keys['a']) dx = -1; if (keys['d']) dx = 1;"
c = c.replace(bad_use_skill, good_use_skill)

# 2. 正しい update(dt) 内に挿入
# 1774行目付近の update 関数の中にある dx = 0, dy = 0; ... のところ
old_update_move = r"(let dx = 0, dy = 0; if \(keys\['w'\]\) dy = -1; if \(keys\['s'\]\) dy = 1; if \(keys\['a'\]\) dx = -1; if \(keys\['d'\]\) dx = 1;\s*if \(dx === 0 && dy === 0\) \{)"
new_update_move = r"""let dx = 0, dy = 0; if (keys['w']) dy = -1; if (keys['s']) dy = 1; if (keys['a']) dx = -1; if (keys['d']) dx = 1;
                const pTile = getTileAt(player.x, player.y);
                if (pTile === 'a') player.y += 150 * dt;
                \1"""
# 実際には capture group 1 に let dx = 0... から含まれているので、2回書くと重複する。正しくは：
new_update_move2 = r"""let dx = 0, dy = 0; if (keys['w']) dy = -1; if (keys['s']) dy = 1; if (keys['a']) dx = -1; if (keys['d']) dx = 1;
                const pTile = getTileAt(player.x, player.y);
                if (pTile === 'a') { player.y += 150 * dt; }
                if (dx === 0 && dy === 0) {"""
# 正規表現で置き換え
pattern_update = r"let dx = 0, dy = 0; if \(keys\['w'\]\) dy = -1; if \(keys\['s'\]\) dy = 1; if \(keys\['a'\]\) dx = -1; if \(keys\['d'\]\) dx = 1;\s*if \(dx === 0 && dy === 0\) \{"
c = re.sub(pattern_update, new_update_move2, c)


# 3. loadScene() の parseInt を修正する
# 1196行目付近: row.push(parseInt(currentScene.tiles[r][c], 36));
old_load = r"row\.push\(parseInt\(currentScene\.tiles\[r\]\[c\],\s*36\)\);"
new_load = """const char = currentScene.tiles[r][c];
                    if (char === 'a' || char === 'v' || char === 'w') row.push(char);
                    else row.push(parseInt(char, 36));"""
c = re.sub(old_load, new_load, c)


# 4. update(dt) の胞子毒処理の修正
# 前回の置換で: if (currentSceneId === 'dungeon_f7' && pTile !== 'v' && pTile !== 0 && pTile !== '0') {
# しかし、pTile は getTileAt で取得するが、上で定義した pTile を使うようにしたので大丈夫。
# ただし、上で定義した pTile がスコープ的に干渉しないか確認。
# さっき `const pTile = getTileAt(player.x, player.y);` を `update` の先頭（移動部分）に入れたが、
# 毒処理はもっと上の `resolveSafetyCollisions()` の直下あたりにあった `isInPit` のところだ。
# 実際には `isInPit` は `update(dt)` 内にある。
# previous apply_hazards.py did:
# c = c.replace(old_pit, new_pit)
# which created `pTile !== 'v'` before pTile is even defined in update!
# This causes ReferenceError: pTile is not defined in update()!

# だから、pTile を isInPit の前で定義するか、getTileAt(player.x, player.y) に戻す。
c = c.replace("pTile !== 'v' && pTile !== 0 && pTile !== '0'", "getTileAt(player.x, player.y) !== 'v' && getTileAt(player.x, player.y) !== 0")

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed loadScene, useSkill, and update logic!")
