// entity.js

// 階層番号を取得するユーティリティ関数
function getFloorLevel() {
    if (!currentSceneId.startsWith('dungeon_f')) return 1;
    return parseInt(currentSceneId.replace('dungeon_f', '')) || 1;
}

class Enemy {
    constructor(x, y, type, id) {
        this.x = x; this.y = y; this.type = type; this.id = id;
        this.isAlive = true; this.vx = 0; this.vy = 0;
        this.hurtTimer = 0; this.attackTimer = 0;
        
        // 階層によるレベルスケーリング（F2なら+5, F3なら+10...）
        const floorLevel = getFloorLevel();
        const levelBonus = (floorLevel - 1) * 5;
        
        if (type === 'slime') { this.hp = 30 + levelBonus*2; this.maxHp = this.hp; this.atk = 5 + levelBonus; this.spd = 50; this.color = '#3b82f6'; this.size = 14; }
        else if (type === 'bat') { this.hp = 20 + levelBonus; this.maxHp = this.hp; this.atk = 8 + levelBonus; this.spd = 80; this.color = '#64748b'; this.size = 10; }
        else if (type === 'skeleton') { this.hp = 50 + levelBonus*3; this.maxHp = this.hp; this.atk = 12 + levelBonus*1.5; this.spd = 40; this.color = '#e2e8f0'; this.size = 16; }
        else if (type === 'wind_slime') { this.hp = 40 + levelBonus*2; this.maxHp = this.hp; this.atk = 10 + levelBonus; this.spd = 90; this.color = '#10b981'; this.size = 14; }
        else if (type === 'boss') { 
            // ボスのステータス
            this.hp = 300 + levelBonus*10; this.maxHp = this.hp; this.atk = 20 + levelBonus*2; this.spd = 60; this.color = '#ef4444'; this.size = 24; 
            this.isBoss = true; 
            // バリアは撤廃（攻撃してくるようにする）
            this.isInvincible = false;
        }
    }

    update(dt) {
        if (!this.isAlive) return;
        if (this.hurtTimer > 0) this.hurtTimer -= dt;
        this.attackTimer -= dt;

        // ボスも通常敵もプレイヤーに向かって移動する（バリアや停止はない）
        const dist = Math.hypot(player.x - this.x, player.y - this.y);
        
        if (dist < 300) { // プレイヤーが近づいたら認識
            const angle = Math.atan2(player.y - this.y, player.x - this.x);
            let nextX = this.x + Math.cos(angle) * this.spd * dt;
            let nextY = this.y + Math.sin(angle) * this.spd * dt;
            
            // 敵の壁抜け防止（固体タイルにぶつかるなら移動をキャンセル）
            const solidTiles = [1, 4, 7, 8, 9, 11]; // 壁、扉など
            const tileAtNextX = getTileAt(nextX, this.y);
            const tileAtNextY = getTileAt(this.x, nextY);

            if (!solidTiles.includes(tileAtNextX)) {
                this.x = nextX;
            }
            if (!solidTiles.includes(tileAtNextY)) {
                this.y = nextY;
            }

            // 攻撃処理
            if (dist < this.size + player.radius + 5 && this.attackTimer <= 0) {
                this.attackTimer = 1.5;
                if (player.state !== PlayerState.DASH) {
                    player.hp -= Math.max(1, this.atk - player.def);
                    player.state = PlayerState.HURT;
                    setTimeout(() => { if (player.state === PlayerState.HURT) player.state = PlayerState.IDLE; }, 300);
                    showToast(`${this.type}の攻撃！ ${Math.max(1, this.atk - player.def)} ダメージ`);
                }
            }
            
            // ボスの遠距離攻撃（ファイアボール等）
            if (this.isBoss && dist > 50 && dist < 200 && this.attackTimer <= 0) {
                this.attackTimer = 2.0;
                enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, this.atk, '#f97316'));
            }
        }
    }

    draw(ctx) {
        if (!this.isAlive) return;
        ctx.fillStyle = this.hurtTimer > 0 ? '#ffffff' : this.color;
        ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI*2); ctx.fill();
        if (this.isBoss) {
            ctx.strokeStyle = '#fef08a'; ctx.lineWidth = 3; ctx.stroke();
            // ボスのHPバー
            ctx.fillStyle = '#000'; ctx.fillRect(this.x - 20, this.y - 35, 40, 6);
            ctx.fillStyle = '#ef4444'; ctx.fillRect(this.x - 20, this.y - 35, 40 * (this.hp / this.maxHp), 6);
        }
    }
}

class EnemyProjectile {
    constructor(x, y, angle, damage, color) {
        this.x = x; this.y = y; this.vx = Math.cos(angle)*150; this.vy = Math.sin(angle)*150;
        this.damage = damage; this.color = color; this.life = 3;
    }
    update(dt) {
        this.x += this.vx * dt; this.y += this.vy * dt; this.life -= dt;
        // 壁に当たったら消滅
        const tile = getTileAt(this.x, this.y);
        if ([1, 4, 7, 8, 9, 11].includes(tile)) {
            this.life = 0;
        }
    }
    draw(ctx) {
        ctx.fillStyle = this.color; ctx.beginPath(); ctx.arc(this.x, this.y, 6, 0, Math.PI*2); ctx.fill();
    }
}

function applyDamageToEnemy(enemy, damage) {
    if (!enemy.isAlive) return;
    enemy.hp -= damage;
    enemy.hurtTimer = 0.2;
    damageParticles.push({x: enemy.x, y: enemy.y, life: 0.5, text: Math.floor(damage)});
    if (enemy.hp <= 0) {
        enemy.isAlive = false;
        player.xp += (enemy.isBoss ? 50 : 10);
        
        // アイテムドロップ
        const r = Math.random();
        if (r < 0.5) player.inventory['スライムの粘液']++;
        else if (r < 0.8) player.inventory['鉄くず']++;
        else if (r < 0.95) player.inventory['風の結晶']++;
        else player.inventory['アビスコア']++;
        
        // クエスト進行
        if (player.activeQuest && (player.activeQuest.target === enemy.type || (player.activeQuest.target === 'boss' && enemy.isBoss))) {
            player.questProgress++;
            showToast(`クエスト進行: ${player.questProgress} / ${player.activeQuest.req}`);
        }

        if (enemy.isBoss) {
            showToast("ボスを撃破した！ 次の階層へのポータルが出現した！", 3000);
            
            // F1ならF2へのポータルを出現させる（ボスの位置に）
            const ec = Math.floor(enemy.x / TILE_SIZE);
            const er = Math.floor(enemy.y / TILE_SIZE);
            const floorNum = getFloorLevel();
            const nextDest = `dungeon_f${floorNum + 1}`;
            
            // 最終階層ならクリア
            if (floorNum >= 7) {
                showToast("全階層クリア！おめでとうございます！", 5000);
                map[er][ec] = 12; // 帰還ポータル
                currentScene.portals.push({ c: ec, r: er, dest: 'city', sc: 40, sr: 56 });
            } else {
                map[er][ec] = 12; // 次の階へ
                currentScene.portals.push({ c: ec, r: er, dest: nextDest, sc: 40, sr: 76 });
            }
        } else {
            showToast(`${enemy.type}を倒した`);
        }
    }
}
