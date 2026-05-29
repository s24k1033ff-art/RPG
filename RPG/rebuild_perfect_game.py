import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()


# 1. 街 (city) とギルド (guild) のポータル修正
city_portals = '''portals: [
                    { c: 40, r: 10, dest: 'guild', sc: 40, sr: 25 },
                    { c: 40, r: 5, dest: 'dungeon_f1', sc: 40, sr: 74 },
                ]'''
html = re.sub(r'\'city\': \{[\s\S]*?portals: \[[\s\S]*?\]', r"'city': { type: 'city', portals: [\n                    { c: 40, r: 10, dest: 'guild', sc: 40, sr: 25 },\n                    { c: 40, r: 5, dest: 'dungeon_f1', sc: 40, sr: 74 },\n                ]", html)

guild_portals = '''portals: [
                    { c: 40, r: 28, dest: 'city', sc: 40, sr: 12 },
                ]'''
html = re.sub(r'\'guild\': \{[\s\S]*?portals: \[[\s\S]*?\]', r"'guild': { type: 'city', portals: [\n                    { c: 40, r: 28, dest: 'city', sc: 40, sr: 12 },\n                ]", html)

# 2. 壁抜け防止
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

# 3. ボスのバリア削除と攻撃追加
# 元のバリアロジック: this.isInvincible = true; bossCrystals.forEach(c => c.active = false); などを無効化
html = html.replace('this.isInvincible = true; bossCrystals.forEach(c => c.active = false);', '// (Boss Barrier removed)')
html = html.replace('const allActive = bossCrystals.length > 0 && bossCrystals.every(c => c.active);', 'const allActive = true;')

boss_logic = '''
                    if (this.attackCooldown <= 0 && Math.random() < 0.05) {
                        enemyProjectiles.push(new Projectile(this.x, this.y, Math.atan2(dy, dx), 150, this.atk, '#f43f5e', 8, true));
                        this.attackCooldown = 1.5;
                    }
'''
html = re.sub(r'if \(this\.type === \'boss\'\) \{[\s\S]*?this\.stateTimer \-= dt;[\s\S]*?\}', boss_logic, html)

# 4. 中ボスとボスのステータス設定
level_scale = '''
                if(type === 'mini_boss') { this.maxHp = 150; this.radius = 20; this.color = '#eab308'; this.speed = 70; this.xp = 150; this.gold = 100; this.atk = 15; this.dropItem = '鉄くず'; }
                else if(type === 'boss') { this.maxHp = 400; this.radius = 32; this.color = '#ef4444'; this.speed = 80; this.xp = 500; this.gold = 300; this.atk = 25; this.dropItem = '記憶の欠片'; }
'''
html = re.sub(r'else if\(type === \'boss\'\) \{.*?\}', level_scale.strip(), html)


# 5. クエストボード＆鍛冶屋入り口の実装
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
html = html.replace('// e: interact', interact_logic + '\n        // e: interact')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')
