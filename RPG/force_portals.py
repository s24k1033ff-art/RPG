import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# loadScene の最後の部分（camera.x = player.x; camera.y = player.y; の後あたり）にポータル強制定義を挿入する
pattern = r"(camera\.x = player\.x;\s*camera\.y = player\.y;)"
replacement = r"""\1

            // --- ポータルの強制初期化と定義 (バグ回避用) ---
            currentScene.portals = [];
            if (id === 'city') {
                currentScene.portals.push({ c: 25, r: 20, dest: 'guild', sc: 10, sr: 13 });
                currentScene.portals.push({ c: 75, r: 30, dest: 'dungeon_f1', sc: 40, sr: 74 });
            } else if (id === 'guild') {
                currentScene.portals.push({ c: 10, r: 14, dest: 'city', sc: 25, sr: 21 });
                currentScene.portals.push({ c: 9, r: 14, dest: 'city', sc: 25, sr: 21 });
                currentScene.portals.push({ c: 11, r: 14, dest: 'city', sc: 25, sr: 21 });
            } else if (id === 'dungeon_f1') {
                currentScene.portals.push({ c: 40, r: 76, dest: 'city', sc: 74, sr: 30 });
            } else if (id.startsWith('dungeon_f')) {
                currentScene.portals.push({ c: 40, r: 76, dest: 'city', sc: 74, sr: 30 });
                // もし各階層でボスを倒していれば、追加のポータルがあるかもしれないが、
                // 初期ロード時には一旦初期化してしまう。ボスを倒した時にプッシュされるので問題なし。
            }
"""
new_c = re.sub(pattern, replacement, c)

# ついでに、update() 内のポータル判定が確実に動くように、currentTile の判定を少し緩和する。
# tile が 12 や 13 ではなくても、現在位置に portal が定義されていれば無条件で飛ぶようにする。
# なぜなら、街マップの 'd' や 'c' は parseInt('d',36)=13 などになるが、
# 何かの拍子でタイルIDが変わっても大丈夫なように。
portal_update_old = r"if \(\(currentTile >= 12 && currentTile <= 16\) && !player\.warping\) \{"
portal_update_new = r"// タイルIDに依存せず、現在座標にポータル定義があれば判定する\n            const pc = Math.floor(player.x / TILE_SIZE);\n            const pr = Math.floor(player.y / TILE_SIZE);\n            const portal = currentScene.portals && currentScene.portals.find(p => p.c === pc && p.r === pr);\n            if (portal && !player.warping) {"

# そしてその下の元の pc, pr, portal 取得ロジックは消すか上書きする
# 元のロジック:
#                const pc = Math.floor(player.x / TILE_SIZE);
#                const pr = Math.floor(player.y / TILE_SIZE);
#                const portal = currentScene.portals.find(p => p.c === pc && p.r === pr);
#                if (portal) {
old_logic = r"const pc = Math\.floor\(player\.x / TILE_SIZE\);\s*const pr = Math\.floor\(player\.y / TILE_SIZE\);\s*const portal = currentScene\.portals\.find\(p => p\.c === pc && p\.r === pr\);\s*if \(portal\) \{"
new_c = re.sub(portal_update_old + r"[\s\S]*?" + old_logic, portal_update_new, new_c)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_c)

print("Injected invincible portal logic!")
