import os
import re

html_path = r"c:\Users\kenka\OneDrive - Chiba Institute of Technology\デスクトップ\RPG\preview_demo.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 置き換える部分の始まりと終わりを見つける
# 開始: const startRoom = [ 
# 終了: const drops = [];
start_marker = "const startRoom = ["
end_marker = "const drops = [];"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("マーカーが見つかりません")
    exit(1)

new_scene_system = """// === シーン（マップ）管理システム ===
        const themes = {
            city: { name: "迷宮都市アビス・エッジ", floor: '#94a3b8', wall: '#78350f', border: '#475569', pit: '#1e293b', spike: '#000', npc: '#fbbf24' },
            guild: { name: "冒険者ギルド", floor: '#d2b48c', wall: '#8b4513', border: '#cd853f', pit: '#000', spike: '#000', npc: '#fbbf24' },
            dungeon: { name: "アビス第一階層", floor: '#0f172a', wall: '#1e293b', border: '#38bdf8', pit: '#020617', spike: '#ef4444', npc: '#38bdf8' }
        };

        const sceneData = {
            'city': {
                width: 40, height: 30, // 2x2画面
                tiles: [
                    "1111111111111111111111111111111111111111",
                    "1111111111111111111111111111111111111111",
                    "1111111110000000011111111111100000000111", // 北の施設群
                    "1111111110000000011111111111100000000111",
                    "1111111110000000011111111111100000000111",
                    "1111111110000000011111111111100000000111",
                    "1111111110000000011111111111100000000111",
                    "1111111110000000011111111111100000000111",
                    "1111111110001300011111111111100014000111", // 13: ギルドドア, 14: 鍛冶屋ドア
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000111111000000111111100000000000000001",
                    "1000100001000000100000100000000000000001",
                    "1000100001000000100000100000000000000001",
                    "1000100001000000100000100000000000000001",
                    "1000101501000000101600100000000000000001", // 15: 魔法屋ドア, 16: 宿屋ドア
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000001200000000000000000000000001", // 12: アビス(ダンジョン)へのポータル
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1111111111111111111111111111111111111111",
                    "1111111111111111111111111111111111111111",
                    "1111111111111111111111111111111111111111"
                ],
                portals: [
                    { c: 12, r: 8, dest: 'guild', sc: 10, sr: 13 },
                    { c: 12, r: 23, dest: 'dungeon_f1', sc: 10, sr: 2 }
                ],
                npcs: [
                    { c: 15, r: 10, id: 'guide', name: "ベテラン冒険者" }
                ],
                enemies: [], chests: [],
                getTheme: () => themes.city
            },
            'guild': {
                width: 20, height: 15,
                tiles: [
                    "11111111111111111111",
                    "10000000000000000001",
                    "10000111100111100001",
                    "10000100000000100001",
                    "10000100060000100001", // (9,4) ギルドマスター
                    "10000111100111100001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000005000000000001", // 碑石(ショップ代わり)
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "10000000000000000001",
                    "11111111111211111111" // (10,14) 出口ポータル
                ],
                portals: [
                    { c: 10, r: 14, dest: 'city', sc: 12, sr: 9 }
                ],
                npcs: [
                    { c: 9, r: 4, id: 'guildmaster', name: "ギルドマスター" }
                ],
                enemies: [], chests: [],
                getTheme: () => themes.guild
            },
            'dungeon_f1': {
                width: 40, height: 30, // アビス第1階層(広大)
                tiles: [
                    "1111111111121111111111111111111111111111", // 北に出口ポータル
                    "1000000000000000000100000000000000000001",
                    "1000000000000000000100000000000000000001",
                    "1000111000000001110100001111111000000001",
                    "1000101002222001010100001000001000000001",
                    "1000101002002001010100001000001000000001",
                    "1000101002002001010000001000001000000001",
                    "1000101002222001010000001110111000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000001111111111111111100111111100001",
                    "1000000001000000000000000100100000100001",
                    "1000000001000000000000000100100330100001",
                    "1000000001000000000000000000100330100001",
                    "1000000001000000000000000000100000100001",
                    "1000000001111111111111111111111111100001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000111111000000000011110000000011110001",
                    "1000100001000000000010010000000010010001",
                    "1000100001000000000010010000000010010001",
                    "1000100001000000000011110000000011110001",
                    "1000100001000000000000000000000000000001",
                    "1000110111000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1000000000000000000000000000000000000001",
                    "1111111111111111111111111111111111111111",
                    "1111111111111111111111111111111111111111",
                    "1111111111111111111111111111111111111111"
                ],
                portals: [
                    { c: 11, r: 0, dest: 'city', sc: 12, sr: 24 }
                ],
                npcs: [],
                enemies: [
                    {c: 8, r: 8, type: 'slime'}, {c: 12, r: 8, type: 'slime'},
                    {c: 30, r: 15, type: 'wind_slime'}, {c: 32, r: 16, type: 'wind_slime'},
                    {c: 10, r: 25, type: 'guardian'}
                ],
                chests: [
                    { c: 35, r: 5, opened: false, keyId: 'gold', color: '#fbbf24' }
                ],
                getTheme: () => themes.dungeon
            }
        };

        // ====== エンティティ定義とマップロードシステム ======
        let MAP_COLS = 0; let MAP_ROWS = 0;
        let map = []; let npcs = []; let enemies = []; let chests = [];
        let currentSceneId = ''; let currentScene = null;

        class Enemy {
            constructor(c, r, type) {
                this.x = (c+0.5)*TILE_SIZE; this.y = (r+0.5)*TILE_SIZE; this.vx = 0; this.vy = 0;
                this.type = type; this.isAlive = true; this.hitStun = 0;
                this.attackCooldown = 0; this.canShoot = (type === 'golem' || type === 'boss' || type === 'guardian');
                if(type === 'slime') { this.hp = 2; this.radius = 12; this.color = '#38bdf8'; this.speed = 100; this.xp = 15; this.gold = 10; }
                else if(type === 'wind_slime') { this.hp = 3; this.radius = 10; this.color = '#10b981'; this.speed = 180; this.xp = 25; this.gold = 15; }
                else if(type === 'guardian') { this.hp = 5; this.radius = 14; this.color = '#fcd34d'; this.speed = 120; this.xp = 40; this.gold = 20; }
                else if(type === 'golem') { this.hp = 8; this.radius = 16; this.color = '#a855f7'; this.speed = 40; this.xp = 50; this.gold = 30; }
                else if(type === 'boss') { this.hp = 20; this.radius = 24; this.color = '#ef4444'; this.speed = 90; this.xp = 200; this.gold = 100; this.isInvincible = true; this.barrierRadius = 35; }
            }
        }

        class EnemyProjectile {
            constructor(x, y, angle, speed, color) {
                this.x = x; this.y = y; this.vx = Math.cos(angle)*speed; this.vy = Math.sin(angle)*speed;
                this.life = 2.0; this.color = color; this.active = true;
            }
            update(dt) {
                this.x += this.vx * dt; this.y += this.vy * dt; this.life -= dt;
                if (getTileAt(this.x, this.y) === 1) this.active = false;
                if (this.active && Math.hypot(this.x - player.x, this.y - player.y) < COLLISION_RADIUS + 4) {
                    player.hp -= 5; this.active = false;
                    showToast("敵の攻撃を受けた！");
                }
            }
            render(ctx) {
                ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, 4, 0, Math.PI*2); ctx.fill();
                ctx.shadowBlur = 10; ctx.shadowColor = this.color; ctx.fill(); ctx.shadowBlur = 0;
            }
        }
        const enemyProjectiles = [];

        function loadScene(id, spawnC, spawnR) {
            currentSceneId = id;
            currentScene = sceneData[id];
            MAP_COLS = currentScene.width;
            MAP_ROWS = currentScene.height;
            map = [];
            for (let r = 0; r < MAP_ROWS; r++) {
                const row = [];
                for (let c = 0; c < MAP_COLS; c++) {
                    row.push(parseInt(currentScene.tiles[r][c], 10));
                }
                map.push(row);
            }
            npcs = currentScene.npcs.map(n => ({ ...n, x: (n.c+0.5)*TILE_SIZE, y: (n.r+0.5)*TILE_SIZE }));
            enemies = currentScene.enemies.map(e => new Enemy(e.c, e.r, e.type));
            chests = currentScene.chests.map(c => ({ ...c, x: (c.c+0.5)*TILE_SIZE, y: (c.r+0.5)*TILE_SIZE }));
            
            enemyProjectiles.length = 0;
            swordSlashes.length = 0;
            damageParticles.length = 0;

            player.x = (spawnC + 0.5) * TILE_SIZE;
            player.y = (spawnR + 0.5) * TILE_SIZE;
            camera.x = player.x; camera.y = player.y;
            
            showToast(currentScene.getTheme().name + " に移動しました");
        }

        const dialogues = {
            'guide': [
                "おい、大丈夫か？ こんな浅層で倒れているとはな...",
                "記憶がないのか？ ここは『アビス』と呼ばれる巨大な迷宮だ。",
                "とりあえず、まずはこの辺りのスライムを狩って勘を取り戻せ。",
                "I, O, K, L キーのスキルを使って戦うんだ。Jで通常攻撃だ。",
                "準備ができたら奥へ進もう。さらなる深層を目指すんだ！"
            ],
            'guildmaster': [
                "よく来たな、冒険者よ。私はギルドマスターだ。",
                "ここは『迷宮都市アビス・エッジ』。",
                "アビスの恵みによって栄え、そして呪われた街だ。",
                "準備ができたら、南のポータルからダンジョンへ向かえ。",
                "健闘を祈る！"
            ]
        };
        let dialogueState = { active: false, lines: [], lineIdx: 0, charIdx: 0, timer: 0 };
"""

new_content = content[:start_idx] + new_scene_system + content[end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Successfully replaced scene logic.")
