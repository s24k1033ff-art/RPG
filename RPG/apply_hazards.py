import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. コンベア床の処理をプレイヤーの移動に追加
# function update(dt) の中にプレイヤー移動処理がある
old_move = r"let dx = 0, dy = 0; if \(keys\['w'\]\) dy = -1; if \(keys\['s'\]\) dy = 1; if \(keys\['a'\]\) dx = -1; if \(keys\['d'\]\) dx = 1;"
new_move = """let dx = 0, dy = 0; if (keys['w']) dy = -1; if (keys['s']) dy = 1; if (keys['a']) dx = -1; if (keys['d']) dx = 1;
            
            // 環境ハザード: コンベア床 (a) と ツタ (v)
            const pTile = getTileAt(player.x, player.y);
            if (pTile === 'a') {
                // コンベアは下向き(南)へ流すとする
                player.y += 150 * dt;
            }
"""
c = re.sub(old_move, new_move, c)

# 2. 視界制限（暗闇マスク）を render() の最後に追加
old_render_end = r"ctx\.restore\(\);\n\s*\}\n\s*function checkInteraction\(\) \{"
new_render_end = """ctx.restore();

            // === 暗闇と視界制限 (F4 & F5) ===
            const timeSec = Date.now() / 1000;
            const isF4 = currentSceneId === 'dungeon_f4';
            const isF5Dark = currentSceneId === 'dungeon_f5' && (timeSec % 10 < 5); // 10秒周期で5秒間暗闇
            
            if (isF4 || isF5Dark) {
                // 半径
                let visRadius = player.currentSoulId === 'Lilith' ? 120 : 80;
                
                ctx.save();
                ctx.fillStyle = 'rgba(0, 0, 0, 0.96)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.globalCompositeOperation = 'destination-out';
                ctx.beginPath();
                ctx.arc(canvas.width/2, canvas.height/2, visRadius, 0, Math.PI*2);
                ctx.fill();
                
                // ぼかし境界
                const grad = ctx.createRadialGradient(canvas.width/2, canvas.height/2, visRadius-20, canvas.width/2, canvas.height/2, visRadius+20);
                grad.addColorStop(0, 'rgba(0,0,0,1)');
                grad.addColorStop(1, 'rgba(0,0,0,0)');
                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(canvas.width/2, canvas.height/2, visRadius+20, 0, Math.PI*2);
                ctx.fill();
                
                ctx.restore();
            }
        }
        function checkInteraction() {"""
c = re.sub(old_render_end, new_render_end, c)

# 3. 胞子毒（F7）の処理を update() に追加
# update(dt) の中のプレイヤーHP処理の辺り
old_pit = r"if \(isInPit\) \{"
new_pit = """// 胞子毒ダメージ (F7の下層)
            if (currentSceneId === 'dungeon_f7' && pTile !== 'v' && pTile !== 0 && pTile !== '0') {
                // pTile が 0(安全地帯) や v(ツタ) でない場合、毒ダメージ
                player.hp -= (player.maxHp * 0.02) * dt; 
            }
            if (isInPit) {"""
c = content = c.replace(old_pit, new_pit)

# 4. コンベア床(a)やツタ(v)の描画ロジックを drawMap() の辺りか getTileAt(), map の描画(render内)に追加する
# function render() の中:
# if (tile === 0 || tile === 2 || tile === 3 || tile === 12) ... のような描画処理があるはず
# 描画処理を調べてから置き換えるのは複雑なので、とりあえず a と v の文字を追加
old_tile_draw = r"if \(tile === 1\) \{ ctx\.fillStyle = theme\.wall;"
new_tile_draw = """if (tile === 'a') { ctx.fillStyle = '#1e3a8a'; } // コンベア
            else if (tile === 'v') { ctx.fillStyle = '#166534'; } // ツタ
            else if (tile === 1) { ctx.fillStyle = theme.wall;"""
c = c.replace(old_tile_draw, new_tile_draw)

# 壁判定 getTileAt は文字列の '1', 'a' なども処理できるように parseInt ではなくそのままにする
# プレビューではparseIntしている場所があるか？ loadScene を見る。
# loadScene で parseInt している部分
old_load = r"row\.push\(parseInt\(currentScene\.tiles\[r\]\[c\],\s*10\)\);"
new_load = """const char = currentScene.tiles[r][c];
                    if (char === 'a' || char === 'v' || char === 'w' || char === 'c') row.push(char);
                    else row.push(parseInt(char, 10));"""
c = c.replace(old_load, new_load)


with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied missing gimmicks successfully!")
