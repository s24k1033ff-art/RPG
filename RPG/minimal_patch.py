import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 敵の壁抜け防止 (Enemy.update内)
# 元のコードに "this.x += this.vx * dt;" が複数ある
wall_collision = '''
                    let nextX = this.x + this.vx * dt; let nextY = this.y + this.vy * dt;
                    let canMove = true;
                    let adjTiles = [
                        getTileAt(nextX - 10, nextY - 10), getTileAt(nextX + 10, nextY - 10),
                        getTileAt(nextX - 10, nextY + 10), getTileAt(nextX + 10, nextY + 10)
                    ];
                    if (adjTiles.some(t => [1,2,4,7,8,9,11].includes(t))) canMove = false;
                    if (canMove) { this.x = nextX; this.y = nextY; }
'''
html = html.replace('this.x += this.vx * dt; this.y += this.vy * dt;', wall_collision)

# 2. ボスのバリア無効化
html = html.replace('this.isInvincible = true; bossCrystals.forEach(c => c.active = false);', '// (Removed Boss Barrier)')

# ボスの攻撃（簡易的）
# "if (this.type === 'boss') {" の中に挿入
boss_atk = '''
                if (this.attackCooldown <= 0 && Math.random() < 0.05) {
                    const dx = player.x - this.x; const dy = player.y - this.y;
                    enemyProjectiles.push(new Projectile(this.x, this.y, Math.atan2(dy, dx), 150, this.atk, '#f43f5e', 8, true));
                    this.attackCooldown = 1.5;
                }
'''
html = html.replace("if (this.type === 'boss') {", "if (this.type === 'boss') {" + boss_atk)

# 3. 中ボスステータス
boss_stats = '''
            else if(type === 'mini_boss') { this.maxHp = 150; this.radius = 20; this.color = '#eab308'; this.speed = 70; this.xp = 150; this.gold = 100; this.atk = 15; this.dropItem = '鉄くず'; }
            else if(type === 'boss') { this.maxHp = 400; this.radius = 32; this.color = '#ef4444'; this.speed = 80; this.xp = 500; this.gold = 300; this.atk = 25; this.dropItem = '記憶の欠片'; }
'''
html = html.replace("else { this.maxHp = 5; this.radius = 15; this.color = '#fff'; this.speed = 60; this.xp = 10; this.gold = 5; }", boss_stats + "\n            else { this.maxHp = 5; this.radius = 15; this.color = '#fff'; this.speed = 60; this.xp = 10; this.gold = 5; }")


# 4. クエストボード＆鍛冶屋入り口の実装
interact_logic = '''
        if (typeof currentSceneId !== "undefined" && currentSceneId === 'guild' && player.y < 5 * TILE_SIZE) {
            player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
            if (!player.activeQuest) {
                const quests = [
                    { id: 1, name: 'スライム討伐', target: 'slime', req: 5, reward: 100 },
                    { id: 2, name: 'コウモリ駆除', target: 'bat', req: 8, reward: 150 },
                    { id: 3, name: 'スケルトン討伐', target: 'skeleton', req: 5, reward: 200 },
                    { id: 4, name: '素材納品', target: '鉄くず', req: 3, reward: 300 },
                    { id: 5, name: 'ボス討伐', target: 'boss', req: 1, reward: 1000 }
                ];
                player.activeQuest = quests[Math.floor(Math.random() * quests.length)];
                player.questProgress = 0;
                dialogueState = { active: true, lines: ["📜 【クエストボード】\\n★ 『" + player.activeQuest.name + "』を受注しました！"], lineIdx: 0, charIdx: 0, timer: 0 };
            } else {
                if (player.activeQuest.target === '鉄くず' && player.inventory['鉄くず'] >= player.activeQuest.req) {
                    player.inventory['鉄くず'] -= player.activeQuest.req;
                    player.gold += player.activeQuest.reward;
                    dialogueState = { active: true, lines: ["📜 【クエストボード】\\n★ 報告完了！ 報酬の【" + player.activeQuest.reward + "G】を獲得！"], lineIdx: 0, charIdx: 0, timer: 0 };
                    player.activeQuest = null; player.questProgress = 0;
                } else if (player.activeQuest.target !== '鉄くず' && player.questProgress >= player.activeQuest.req) {
                    player.gold += player.activeQuest.reward;
                    dialogueState = { active: true, lines: ["📜 【クエストボード】\\n★ 報告完了！ 報酬の【" + player.activeQuest.reward + "G】を獲得！"], lineIdx: 0, charIdx: 0, timer: 0 };
                    player.activeQuest = null; player.questProgress = 0;
                } else {
                    dialogueState = { active: true, lines: ["📜 【クエストボード】\\n★ 進行度: " + player.questProgress + "/" + player.activeQuest.req], lineIdx: 0, charIdx: 0, timer: 0 };
                }
            }
            document.getElementById('dialogueName').textContent = "クエストボード"; 
            document.getElementById('dialogueOverlay').classList.add('show');
            return;
        }

        if (typeof currentSceneId !== "undefined" && currentSceneId === 'city' && Math.hypot(60*TILE_SIZE - player.x, 20*TILE_SIZE - player.y) < 150) {
            player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
            let cost = player.weaponLevel * 100;
            if (player.inventory['鉄くず'] >= 1 && player.gold >= cost) {
                player.inventory['鉄くず']--; player.gold -= cost;
                player.weaponLevel++; player.armorLevel++; player.atk += 2; player.def += 1;
                dialogueState = { active: true, lines: ["🔨 【鍛冶屋】\\nおう！強化完了だ！武器Lv " + player.weaponLevel + " になったぜ！"], lineIdx: 0, charIdx: 0, timer: 0 };
            } else {
                dialogueState = { active: true, lines: ["🔨 【鍛冶屋】\\n素材（鉄くず1個）とゴールド（" + cost + "G）が足りねえな。"], lineIdx: 0, charIdx: 0, timer: 0 };
            }
            document.getElementById('dialogueName').textContent = "鍛冶屋"; 
            document.getElementById('dialogueOverlay').classList.add('show');
            return;
        }
'''
html = html.replace('function triggerInteract() {', 'function triggerInteract() {\n' + interact_logic)


# 5. 強制ポータル（update関数内に差し込む）
force_portals = '''
        if (typeof currentSceneId !== 'undefined' && player) {
            if (currentSceneId === 'guild' && player.y > 28 * TILE_SIZE) {
                loadScene('city'); player.x = 40 * TILE_SIZE; player.y = 12 * TILE_SIZE;
            } else if (currentSceneId === 'city' && player.y < 12 * TILE_SIZE && player.x > 38 * TILE_SIZE && player.x < 42 * TILE_SIZE) {
                loadScene('guild'); player.x = 40 * TILE_SIZE; player.y = 25 * TILE_SIZE;
            } else if (currentSceneId === 'city' && player.y > 50 * TILE_SIZE) {
                loadScene('dungeon_f1'); player.x = 40 * TILE_SIZE; player.y = 74 * TILE_SIZE;
            } else if (currentSceneId.startsWith('dungeon') && player.y > 75 * TILE_SIZE) {
                loadScene('city'); player.x = 40 * TILE_SIZE; player.y = 30 * TILE_SIZE;
            }
        }
'''
html = html.replace('function update() {', 'function update() {\n' + force_portals)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Minimal safe patch applied.')
