import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 壁抜け防止
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

# 2. ボスのバリア無効化と攻撃強化
html = html.replace('this.isInvincible = true; bossCrystals.forEach(c => c.active = false);', '// (Removed Boss Barrier)')

# 3. 鍛冶屋とクエスト
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
html = re.sub(r'else if \(npc\.id === \'blacksmith_master\'\) \{[\s\S]*?\}', forge_logic.strip(), html)

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

# 4. 全画面とリサイズ
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

# 5. 枠の描画
border_render = '''
                    if (tile === 1 || tile === 2 || tile === 'border') { 
                        ctx.fillStyle = theme.border || '#475569'; 
                        ctx.fillRect(tx, ty, TILE_SIZE, TILE_SIZE); 
                        ctx.strokeStyle = '#000'; ctx.lineWidth = 1; ctx.strokeRect(tx, ty, TILE_SIZE, TILE_SIZE); 
                    }
'''
html = re.sub(r'if \(tile === 1\) \{ ctx\.fillStyle = theme\.wall;.*?\}', border_render, html)

# 6. 敵のレベルスケーリング (+5)
level_scale = '''
                let levelBonus = 0;
                if (typeof currentSceneId === 'string' && currentSceneId.startsWith('dungeon_f')) {
                    levelBonus = parseInt(currentSceneId.replace('dungeon_f', '')) || 1;
                }
                
                if(type === 'slime') { this.maxHp = 2 + levelBonus*5; this.radius = 12; this.color = '#38bdf8'; this.speed = 80; this.xp = 15; this.gold = 10; this.dropItem = 'スライムの粘液'; }
                else if(type === 'wind_slime') { this.maxHp = 3 + levelBonus*5; this.radius = 10; this.color = '#10b981'; this.speed = 150; this.xp = 25; this.gold = 15; this.dropItem = '風の翼'; }
                else if(type === 'golem') { this.maxHp = 5 + levelBonus*8; this.radius = 20; this.color = '#9ca3af'; this.speed = 40; this.xp = 40; this.gold = 30; this.dropItem = '鉄くず'; }
                else if(type === 'guardian') { this.maxHp = 8 + levelBonus*10; this.radius = 24; this.color = '#fbbf24'; this.speed = 60; this.xp = 80; this.gold = 50; this.dropItem = '鉄くず'; }
                else if(type === 'skeleton') { this.maxHp = 15 + levelBonus*10; this.radius = 15; this.color = '#f1f5f9'; this.speed = 90; this.xp = 60; this.gold = 40; this.dropItem = '鉄くず'; }
                else if(type === 'bat') { this.maxHp = 10 + levelBonus*5; this.radius = 12; this.color = '#a78bfa'; this.speed = 120; this.xp = 40; this.gold = 25; this.dropItem = '風の翼'; }
                else if(type === 'boss') { this.maxHp = 300 + levelBonus*50; this.radius = 32; this.color = '#ef4444'; this.speed = 60; this.xp = 500; this.gold = 300; this.dropItem = '魔物の肉'; }
                else { this.maxHp = 5; this.radius = 15; this.color = '#fff'; this.speed = 60; this.xp = 10; this.gold = 5; }
'''
html = re.sub(r'if\(type === \'slime\'\) \{[\s\S]*?else \{ this\.maxHp = 3; this\.radius = 15; this\.color = \'#fff\'; this\.speed = 50; this\.xp = 10; this\.gold = 5; \}', level_scale.strip(), html)


# 7. 各階層のスタート地点ポータル
# dungeon_f1 などの portals 配列に強制的に { c:40, r:76, dest:'city', ... } などを挿入するのではなく、
# スポーン位置を読み取って配置する。が、面倒なので単純に (40, 76) 等に青いポータルを置く。
# \1 にマッチするのは 'dungeon_f1': { ... 
def replacer(m):
    return m.group(1) + "portals: [\n                    { c: 40, r: 76, dest: 'city', sc: 74, sr: 30, color: '#4facfe' },"

# html 内のすべての dungeon_f\d+ ブロックに対して portals を書き換える
dungeons = ['dungeon_f1', 'dungeon_f2', 'dungeon_f3', 'dungeon_f4', 'dungeon_f5', 'dungeon_f6', 'dungeon_f7']
for d in dungeons:
    # 該当ダンジョンの portals: [ を探して置換
    pattern = r'(\'' + d + r'\': \{[\s\S]*?)portals: \['
    html = re.sub(pattern, replacer, html, count=1)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Success')
