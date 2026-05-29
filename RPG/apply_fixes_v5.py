import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 敵の壁抜け防止 (Enemy.update内)
html = re.sub(
    r'this\.x \+= this\.vx;\s*this\.y \+= this\.vy;',
    r'''
        let nextX = this.x + this.vx; let nextY = this.y + this.vy;
        let canMove = true;
        let adjTiles = [
            getTileAt(nextX - 10, nextY - 10), getTileAt(nextX + 10, nextY - 10),
            getTileAt(nextX - 10, nextY + 10), getTileAt(nextX + 10, nextY + 10)
        ];
        if (adjTiles.some(t => [1,2,4,7,8,9,11].includes(t))) canMove = false;
        if (canMove) { this.x = nextX; this.y = nextY; }
    ''',
    html
)


# 2. 敵のレベルスケーリング
level_scale = '''
                let levelBonus = 0;
                if (typeof currentSceneId === 'string' && currentSceneId.startsWith('dungeon_f')) {
                    levelBonus = parseInt(currentSceneId.replace('dungeon_f', '')) || 1;
                }
                
                if (type === 'slime') { this.hp = 30 + levelBonus * 5; this.atk = 5 + levelBonus; this.spd = 40 + levelBonus*2; this.color = '#4ade80'; this.size = 12; this.xp = 10 + levelBonus*5; this.gold = 5 + levelBonus*2; }
                else if (type === 'bat') { this.hp = 20 + levelBonus * 5; this.atk = 8 + levelBonus; this.spd = 80 + levelBonus*3; this.color = '#a78bfa'; this.size = 8; this.xp = 15 + levelBonus*5; this.gold = 10 + levelBonus*3; }
                else if (type === 'skeleton') { this.hp = 50 + levelBonus * 8; this.atk = 12 + levelBonus*2; this.spd = 50 + levelBonus*2; this.color = '#f1f5f9'; this.size = 14; this.xp = 25 + levelBonus*5; this.gold = 15 + levelBonus*3; }
                else if (type === 'boss') { this.hp = 500 + levelBonus * 50; this.atk = 20 + levelBonus*3; this.spd = 60; this.color = '#f43f5e'; this.size = 25; this.xp = 500; this.gold = 300; }
                else { this.hp = 30; this.atk = 5; this.spd = 40; this.color = '#fff'; this.size = 12; this.xp = 10; this.gold = 5; }
                this.maxHp = this.hp;
'''
html = re.sub(r'if \(type === \'slime\'\) \{[\s\S]*?this\.maxHp = this\.hp;', level_scale, html)


# 3. ボスのバリア撤廃（クリスタル無敵をなくし、常に追尾＆攻撃）
boss_logic = '''
                    if (this.attackCooldown <= 0 && Math.random() < 0.05) {
                        enemyProjectiles.push(new Projectile(this.x, this.y, Math.atan2(dy, dx), 150, this.atk, '#f43f5e', 8, true));
                        this.attackCooldown = 2.0;
                    }
'''
html = re.sub(r'if \(this\.type === \'boss\'\) \{[\s\S]*?this\.stateTimer \-= dt;[\s\S]*?\}', boss_logic, html)


# 4. 鍛冶屋の装備強化とクエスト増加 (triggerInteract内)
forge_logic = '''
                else if (npc.id === 'blacksmith_master') {
                    let cost = player.weaponLevel * 100;
                    if (player.inventory['鉄くず'] >= 1 && player.gold >= cost) {
                        player.inventory['鉄くず']--; player.gold -= cost;
                        player.weaponLevel++; player.armorLevel++; player.atk += 2; player.def += 1;
                        lines = ["おう！強化完了だ！武器Lv " + player.weaponLevel + " になったぜ！"];
                    } else {
                        lines = ["素材（鉄くず1個）とゴールド（" + cost + "G）が足りねえな。"];
                    }
                }
'''
html = re.sub(r'else if \(npc\.id === \'blacksmith_master\'\) \{[\s\S]*?\}', forge_logic, html)


quest_board = '''
        const adjTiles = [getTileAt(player.x, player.y), getTileAt(player.x, player.y-18), getTileAt(player.x, player.y+18), getTileAt(player.x-18, player.y), getTileAt(player.x+18, player.y)];
        if (adjTiles.includes(17) || (typeof currentSceneId !== "undefined" && currentSceneId === 'guild' && player.y < 3 * TILE_SIZE)) {
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
            } else if (player.activeQuest.target === '鉄くず' && player.inventory['鉄くず'] >= player.activeQuest.req) {
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
            document.getElementById('dialogueName').textContent = "クエストボード"; 
            document.getElementById('dialogueOverlay').classList.add('show');
            return;
        }
'''
html = html.replace('// e: interact', quest_board + '\n        // e: interact')


# 5. 全画面表示とESC (keydown内)
fs_logic = '''
    if (e.key === 'f' || e.key === 'F') {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => console.log(err));
        } else {
            document.exitFullscreen();
        }
    }
    if (e.key === 'Escape') {
        if (document.fullscreenElement) document.exitFullscreen();
'''
html = re.sub(r'if \(e\.key === \'Escape\'\) \{', fs_logic, html)

resize_logic = '''
function resizeCanvas() {
    if (document.fullscreenElement) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    } else {
        canvas.width = 1024;
        canvas.height = 768;
    }
}
window.addEventListener('resize', resizeCanvas);
'''
html = html.replace('function init() {', resize_logic + '\n        function init() {')


# 6. 建物の枠描画 (render内)
border_render = '''
                    if (tile === 1 || tile === 2 || tile === 'border') { 
                        ctx.fillStyle = theme.border || '#475569'; 
                        ctx.fillRect(tx, ty, TILE_SIZE, TILE_SIZE); 
                        ctx.strokeStyle = '#000'; ctx.lineWidth = 1; ctx.strokeRect(tx, ty, TILE_SIZE, TILE_SIZE); 
                    }
'''
html = re.sub(r'if \(tile === 1\) \{ ctx\.fillStyle = theme\.wall;.*?\}', border_render, html)


# 7. 各階層のスタート地点にポータル追加 (sceneData内のportals拡張)
# 階層の最初（F1〜F7のどれか）には必ず dest: 'city' を追加する
def add_portal(m):
    # すでに dest: 'city' があればそのまま
    if 'dest: \'city\'' in m.group(0) or 'dest: "city"' in m.group(0):
        return m.group(0)
    # なければ追加
    return "portals: [\n                    { c: 40, r: 76, dest: 'city', sc: 40, sr: 30, color: '#4facfe' },"

html = re.sub(r'portals: \[', add_portal, html)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')
