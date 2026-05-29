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
draw_room(40, 35, 16, 12) # y=29~40

# HUB北側に壁を作り、中央の通路(x=38~41)だけ開けるが、そこを青扉(4)で塞ぐ
for x in range(32, 48):
    lines[29][x] = '1'
lines[29][38] = '4'
lines[29][39] = '4'
lines[29][40] = '4'
lines[29][41] = '4'

# [15] 審判の交差点 (40, 20)
draw_room(40, 20, 10, 8) # y=16~23, x=35~44
# 交差点からHUBへの合流 (y=23~29)
draw_room(40, 26, 4, 8)  # y=22~29, x=38~41

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
draw_room(60, 20, 10, 4) # 中ボスから居住区

# 居住区から審判の交差点への一方通行（段差=穴など）
draw_room(48, 20, 10, 4) # x=43~52

# HUBから西への通路
draw_room(25, 35, 15, 4) # x=17~32, y=33~36

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
draw_room(40, 8, 20, 14) # y=1~14, x=30~49
# ボス部屋手前の通路
draw_room(40, 17, 6, 6)  # y=14~19, x=37~42

# [14] 崩落した抜け道（ショトカ）
draw_room(25, 45, 6, 20) # y=35~54, x=22~27
draw_room(32, 55, 10, 4) # 回廊へ x=27~36, y=53~56
# 紫扉（ショトカ鍵）
for y in range(53, 57):
    lines[y][30] = '9'

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
out += "],\n"

with open('map_out_fixed.txt', 'w', encoding='utf-8') as f:
    f.write(out)

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"'dungeon_f1':\s*\{\s*width:\s*80,\s*height:\s*80,[\s\S]*?getTheme:\s*\(\)\s*=>\s*themes\.dungeon\s*\}"
replacement = "'dungeon_f1': {\n                width: 80, height: 80,\n                " + out + "                getTheme: () => themes.dungeon\n            }"

new_content = re.sub(pattern, replacement, content)

# ボスのAIから isInvincible フラグを剥奪し、純粋に攻撃してくるようにする
# type === 'boss' の箇所を修正
boss_ai_pattern = r"else if \(this\.type === 'boss'\) \{[\s\S]*?this\.x \+= this\.vx \* dt; this\.y \+= this\.vy \* dt;\s*\}"
boss_ai_replacement = r"""else if (this.type === 'boss') {
                    // ボスのバリアギミックを削除し、純粋な追尾と攻撃AIにする
                    this.isInvincible = false;
                    if (this.hitStun <= 0) {
                        // プレイヤーへ接近
                        if (dist < 400 && dist > 150) {
                            this.vx = Math.cos(angle) * this.speed * 0.8;
                            this.vy = Math.sin(angle) * this.speed * 0.8;
                        } else {
                            this.vx *= 0.9; this.vy *= 0.9;
                        }
                        
                        this.attackCooldown -= dt;
                        if (this.attackCooldown <= 0 && dist < 350) {
                            this.attackCooldown = 1.0 + Math.random() * 0.5;
                            // 扇状の3WAY弾
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, 250, this.color));
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle + 0.3, 250, this.color));
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle - 0.3, 250, this.color));
                            
                            // ときどき全方位弾
                            if (Math.random() < 0.4) {
                                for(let i=0; i<8; i++) enemyProjectiles.push(new EnemyProjectile(this.x, this.y, (Math.PI/4)*i, 150, this.color));
                            }
                            
                            // プレイヤーに向かって突進
                            if (Math.random() < 0.3) {
                                this.vx = Math.cos(angle) * 600;
                                this.vy = Math.sin(angle) * 600;
                            }
                        }
                    }
                    this.x += this.vx * dt; this.y += this.vy * dt;
                }"""
new_content = re.sub(boss_ai_pattern, boss_ai_replacement, new_content)

# コンストラクタ内のボスの設定から isInvincible = true; などを消す
init_pattern = r"else if\(type === 'boss'\) \{ this\.maxHp = 300; this\.radius = 32; this\.color = '#ef4444'; this\.speed = 110; this\.xp = 500; this\.gold = 300; this\.isInvincible = true; this\.barrierRadius = 45; this\.dropItem = 'アビスコア'; \}"
init_replacement = r"else if(type === 'boss') { this.maxHp = 300; this.radius = 32; this.color = '#ef4444'; this.speed = 110; this.xp = 500; this.gold = 300; this.dropItem = 'アビスコア'; }"
new_content = re.sub(init_pattern, init_replacement, new_content)

# 描画の isInvincible 用サークルを消す
render_pattern = r"if \(this\.isInvincible\) \{\s*ctx\.beginPath\(\); ctx\.arc\(this\.x, this\.y, this\.barrierRadius, 0, Math\.PI \* 2\); ctx\.strokeStyle = 'rgba\(56, 189, 248, 0\.8\)'; ctx\.lineWidth = 3; ctx\.stroke\(\);\s*ctx\.fillStyle = 'rgba\(56, 189, 248, 0\.15\)'; ctx\.fill\(\);\s*\}"
new_content = re.sub(render_pattern, "", new_content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Map logic and boss logic fixed.")
