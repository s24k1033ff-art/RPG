import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 敵の壁抜け防止 (Enemy.update内)
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
# 複数箇所あるのですべて置換する
html = html.replace('this.x += this.vx * dt; this.y += this.vy * dt;', wall_collision)

# 2. ボスのバリア無効化
boss_inv = 'this.isInvincible = true; bossCrystals.forEach(c => c.active = false);'
html = html.replace(boss_inv, '// (Removed Boss Barrier)')


# 3. 鍛冶屋の装備強化
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
# "else if (npc.id === 'blacksmith_master')" を探して上書きするが、文字化けを含む行を置換する。
# NPCのidでマッチさせる
html = re.sub(r'else if \(npc\.id === \'blacksmith_master\'\) \{[\s\S]*?\}', forge_logic.strip(), html)


# 4. クエストボード
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
html = html.replace("if (e.key === 'Escape') {", fs_logic)

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
# ギルドから出られない問題を防止するため、dungeon_f1 などだけ対象にする
def add_portal(m):
    return "portals: [\n                    { c: 40, r: 76, dest: 'city', sc: 40, sr: 30, color: '#4facfe' },"

# 特定の階層（dungeon_f...）の portals: [ にだけポータルを追加
html = re.sub(r'(\'dungeon_f\d+\': \{[\s\S]*?)portals: \[', r'\1' + "portals: [\n                    { c: 40, r: 76, dest: 'city', sc: 40, sr: 30, color: '#4facfe' },", html)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')
