import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 扉の判定を修正（tile === 4 は 'start' と 'forest' の両方を要求）
door_pattern = r"""                    if \(tile === 4\) \{ reqKey = 'start'; keyName = '青の鍵'; \}
                    else if \(tile === 8\) \{ reqKey = 'forest'; keyName = '緑の鍵'; \}
                    else if \(tile === 9\) \{ reqKey = 'crystal'; keyName = '紫の鍵'; \}
                    else if \(tile === 7\) \{ reqKey = 'temple'; keyName = '赤の鍵'; \}

                    if \(player\.keys\[reqKey\]\) \{
                        player\.keys\[reqKey\] = false; // 消費"""

door_replacement = r"""                    if (tile === 4) { reqKey = 'double'; keyName = '双龍の瞳（東西の瞳）'; }
                    else if (tile === 8) { reqKey = 'forest'; keyName = '東の瞳（緑の鍵）'; }
                    else if (tile === 9) { reqKey = 'crystal'; keyName = '紫の鍵'; }
                    else if (tile === 7) { reqKey = 'temple'; keyName = '赤の鍵'; }

                    let canOpen = false;
                    if (tile === 4) {
                        if (player.keys['start'] && player.keys['forest']) {
                            canOpen = true;
                            // 消費しないか、消費するか（今回は消費する）
                            player.keys['start'] = false; player.keys['forest'] = false;
                        }
                    } else if (player.keys[reqKey]) {
                        canOpen = true;
                        player.keys[reqKey] = false;
                    }

                    if (canOpen) {"""

content = re.sub(door_pattern, door_replacement, content)

# 2. 中ボスの定義を追加 (Enemyのコンストラクタ)
init_pattern = r"else if\(type === 'boss'\) \{ this\.maxHp = 300;"
init_replacement = r"else if(type === 'mini_boss') { this.maxHp = 150; this.radius = 24; this.color = '#f97316'; this.speed = 100; this.xp = 200; this.gold = 150; this.dropItem = '中ボスの牙'; }\n                else if(type === 'boss') { this.maxHp = 300;"
content = re.sub(init_pattern, init_replacement, content)

# 3. 中ボスの挙動を追加 (Enemyのupdate)
update_pattern = r"else if \(this\.type === 'boss'\) \{"
update_replacement = r"""else if (this.type === 'mini_boss') {
                    // 中ボスの挙動（バリアなし、突進と弾幕）
                    if (this.hitStun <= 0) {
                        if (dist < 300 && dist > 100) {
                            this.vx = Math.cos(angle) * this.speed;
                            this.vy = Math.sin(angle) * this.speed;
                        } else {
                            this.vx *= 0.9; this.vy *= 0.9;
                        }
                        this.attackCooldown -= dt;
                        if (this.attackCooldown <= 0 && dist < 250) {
                            this.attackCooldown = 1.5;
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, 200, this.color));
                            if (Math.random() < 0.3) {
                                this.vx = Math.cos(angle) * 400; this.vy = Math.sin(angle) * 400;
                            }
                        }
                    }
                    this.move(dt);
                }
                else if (this.type === 'boss') {"""
content = re.sub(update_pattern, update_replacement, content)

# 4. マップデータのボスを中ボスに変更 (c:70, r:20)
map_boss_pattern = r"\{ c: 70, r: 20, type: 'boss' \}"
map_boss_replacement = r"{ c: 70, r: 20, type: 'mini_boss' }"
content = re.sub(map_boss_pattern, map_boss_replacement, content)

# 5. ボス討伐時のポータル生成処理を確認（変更なしで boss のみ反応するはず）
# 元の処理: if (enemy.type === 'boss') { ポータル生成 } 
# mini_boss には反応しないので大丈夫

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Boss and MiniBoss distinguished.")
