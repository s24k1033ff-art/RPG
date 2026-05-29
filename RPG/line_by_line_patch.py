import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = 0

for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
    
    # 1. 街のポータル
    if "'city': {" in line:
        new_lines.append(line)
        # 次の行以降に portals: [ があるはず
        j = 1
        while j < 50:
            if "portals: [" in lines[i+j]:
                # 街のポータルを強制上書き
                lines[i+j] = "                portals: [\n                    { c: 40, r: 10, dest: 'guild', sc: 40, sr: 25 },\n                    { c: 40, r: 5, dest: 'dungeon_f1', sc: 40, sr: 74 }\n                ],\n"
                lines[i+j+1] = ""
                lines[i+j+2] = ""
                break
            j += 1
        continue
    
    # 2. ギルドのポータル
    if "'guild': {" in line:
        new_lines.append(line)
        j = 1
        while j < 50:
            if "portals: [" in lines[i+j]:
                lines[i+j] = "                portals: [\n                    { c: 40, r: 28, dest: 'city', sc: 40, sr: 12 }\n                ],\n"
                lines[i+j+1] = ""
                lines[i+j+2] = ""
                break
            j += 1
        continue
        
    # 3. ボスのバリア無効化
    if "this.isInvincible = true; bossCrystals.forEach(c => c.active = false);" in line:
        new_lines.append(line.replace("this.isInvincible = true; bossCrystals.forEach(c => c.active = false);", "// Removed boss barrier"))
        continue
        
    # 4. ボスの攻撃追加
    if "if (this.type === 'boss') {" in line:
        new_lines.append(line)
        # 次にくる this.stateTimer -= dt; までの間に攻撃ロジックを入れる
        # 簡易的に、行の真下に挿入する
        attack_logic = '''
                    if (this.attackCooldown <= 0 && Math.random() < 0.05) {
                        const dx = player.x - this.x; const dy = player.y - this.y;
                        enemyProjectiles.push(new Projectile(this.x, this.y, Math.atan2(dy, dx), 150, this.atk, '#f43f5e', 8, true));
                        this.attackCooldown = 1.5;
                    }
'''
        new_lines.append(attack_logic)
        continue
        
    # 5. 壁抜け
    if "this.x += this.vx * dt; this.y += this.vy * dt;" in line:
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
        new_lines.append(wall_collision)
        continue
        
    # 6. クエストボードと鍛冶屋 (triggerInteract)
    if "function triggerInteract() {" in line:
        new_lines.append(line)
        quest_logic = '''
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
        new_lines.append(quest_logic)
        continue

    # 7. 中ボスのステータス設定
    if "if(type === 'slime') {" in line:
        new_lines.append(line)
        # 次行あたりにミニボスの設定を挟む
        new_lines.append("                else if(type === 'mini_boss') { this.maxHp = 150; this.radius = 20; this.color = '#eab308'; this.speed = 70; this.xp = 150; this.gold = 100; this.atk = 15; this.dropItem = '鉄くず'; }\n")
        continue

    new_lines.append(line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Line-by-line patch applied.')
