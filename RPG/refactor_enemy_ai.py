import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

enemy_class = """        class Enemy {
            constructor(c, r, type) {
                this.spawnX = (c+0.5)*TILE_SIZE; this.spawnY = (r+0.5)*TILE_SIZE;
                this.x = this.spawnX; this.y = this.spawnY; this.vx = 0; this.vy = 0;
                this.type = type; this.isAlive = true; this.isDead = false; this.respawnTimer = 0;
                this.hitStun = 0; this.attackCooldown = 0;
                this.state = 'idle'; this.stateTimer = 0;
                
                this.canShoot = (type === 'golem' || type === 'boss' || type === 'guardian' || type === 'skeleton');
                
                if(type === 'slime') { this.maxHp = 2; this.radius = 12; this.color = '#38bdf8'; this.speed = 80; this.xp = 15; this.gold = 10; this.dropItem = 'スライムの粘液'; }
                else if(type === 'wind_slime') { this.maxHp = 3; this.radius = 10; this.color = '#10b981'; this.speed = 150; this.xp = 25; this.gold = 15; this.dropItem = '風の結晶'; }
                else if(type === 'guardian') { this.maxHp = 5; this.radius = 14; this.color = '#fcd34d'; this.speed = 100; this.xp = 40; this.gold = 20; this.dropItem = '鉄くず'; }
                else if(type === 'golem') { this.maxHp = 8; this.radius = 16; this.color = '#a855f7'; this.speed = 40; this.xp = 50; this.gold = 30; this.dropItem = '魔法の石板'; }
                else if(type === 'bat') { this.maxHp = 2; this.radius = 8; this.color = '#94a3b8'; this.speed = 160; this.xp = 20; this.gold = 10; this.dropItem = 'コウモリの羽'; }
                else if(type === 'skeleton') { this.maxHp = 4; this.radius = 12; this.color = '#f1f5f9'; this.speed = 90; this.xp = 30; this.gold = 15; this.dropItem = '骨のかけら'; }
                else if(type === 'boss') { this.maxHp = 300; this.radius = 32; this.color = '#ef4444'; this.speed = 110; this.xp = 500; this.gold = 300; this.isInvincible = true; this.barrierRadius = 45; this.dropItem = 'アビスコア'; }
                
                this.hp = this.maxHp;
            }

            update(dt) {
                if (this.isDead) {
                    this.respawnTimer -= dt;
                    if (this.respawnTimer <= 0) {
                        this.isDead = false; this.isAlive = true;
                        this.x = this.spawnX; this.y = this.spawnY;
                        this.hp = this.maxHp; this.state = 'idle';
                    }
                    return;
                }

                if (this.hitStun > 0) {
                    this.hitStun -= dt;
                    this.x += this.vx * dt; this.y += this.vy * dt;
                    this.vx *= 0.9; this.vy *= 0.9;
                    return;
                }

                this.stateTimer -= dt;
                const dist = Math.hypot(this.x - player.x, this.y - player.y);
                const angle = Math.atan2(player.y - this.y, player.x - this.x);

                if (this.type === 'slime' || this.type === 'wind_slime') {
                    if (this.state === 'idle' || this.state === 'chase') {
                        if (dist < 120 && this.stateTimer <= 0) {
                            this.state = 'prepare_attack'; this.stateTimer = 0.5; this.vx = 0; this.vy = 0;
                        } else {
                            this.state = 'chase';
                            if (dist < 300) { this.vx = Math.cos(angle)*this.speed; this.vy = Math.sin(angle)*this.speed; }
                            else { this.vx = 0; this.vy = 0; }
                        }
                    } else if (this.state === 'prepare_attack' && this.stateTimer <= 0) {
                        this.state = 'attacking'; this.stateTimer = 0.8;
                        this.vx = Math.cos(angle)*this.speed*3; this.vy = Math.sin(angle)*this.speed*3;
                    } else if (this.state === 'attacking' && this.stateTimer <= 0) {
                        this.state = 'cooldown'; this.stateTimer = 1.0; this.vx = 0; this.vy = 0;
                    } else if (this.state === 'cooldown' && this.stateTimer <= 0) {
                        this.state = 'idle';
                    }
                    if (this.state !== 'prepare_attack') { this.x += this.vx * dt; this.y += this.vy * dt; }
                }
                else if (this.type === 'bat') {
                    if (this.state === 'idle' || this.state === 'chase') {
                        if (dist < 150 && this.stateTimer <= 0) {
                            this.state = 'attacking'; this.stateTimer = 0.6;
                            this.vx = Math.cos(angle)*this.speed*2.5; this.vy = Math.sin(angle)*this.speed*2.5;
                        } else {
                            this.state = 'chase';
                            if (dist < 350) {
                                const targetAngle = angle + Math.sin(Date.now()*0.003)*1.5;
                                this.vx = Math.cos(targetAngle)*this.speed; this.vy = Math.sin(targetAngle)*this.speed;
                            } else { this.vx = 0; this.vy = 0; }
                        }
                    } else if (this.state === 'attacking' && this.stateTimer <= 0) {
                        this.state = 'cooldown'; this.stateTimer = 1.5;
                        this.vx = -Math.cos(angle)*this.speed; this.vy = -Math.sin(angle)*this.speed;
                    } else if (this.state === 'cooldown' && this.stateTimer <= 0) {
                        this.state = 'idle';
                    }
                    this.x += this.vx * dt; this.y += this.vy * dt;
                }
                else if (this.type === 'skeleton') {
                    if (this.state === 'idle' || this.state === 'chase') {
                        if (dist < 200 && dist > 100) {
                            this.vx = 0; this.vy = 0;
                            if (this.stateTimer <= 0) { this.state = 'prepare_attack'; this.stateTimer = 0.5; }
                        } else if (dist <= 100) {
                            this.vx = -Math.cos(angle)*this.speed*0.8; this.vy = -Math.sin(angle)*this.speed*0.8;
                        } else if (dist < 400) {
                            this.vx = Math.cos(angle)*this.speed; this.vy = Math.sin(angle)*this.speed;
                        } else { this.vx = 0; this.vy = 0; }
                    } else if (this.state === 'prepare_attack' && this.stateTimer <= 0) {
                        this.state = 'cooldown'; this.stateTimer = 2.0;
                        enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, 300, '#e2e8f0'));
                    } else if (this.state === 'cooldown' && this.stateTimer <= 0) {
                        this.state = 'idle';
                    }
                    this.x += this.vx * dt; this.y += this.vy * dt;
                }
                else if (this.type === 'boss') {
                    const allActive = bossCrystals.length > 0 && bossCrystals.every(c => c.active);
                    if (allActive && this.isInvincible) { this.isInvincible = false; this.hitStun = 5.0; showToast("結界崩壊！ボスがダウン！"); }
                    
                    if (this.isInvincible) {
                        if (Math.hypot(this.x - player.x, this.y - player.y) < this.barrierRadius + COLLISION_RADIUS) {
                            const ang = Math.atan2(player.y - this.y, player.x - this.x); player.vx = Math.cos(ang)*500; player.vy = Math.sin(ang)*500; player.hp -= 5; showToast("無敵バリアに弾かれた！");
                        }
                        this.vx = 0; this.vy = 0;
                    } else if (this.hitStun <= 0 && !this.isInvincible) { 
                        this.isInvincible = true; bossCrystals.forEach(c => c.active = false); showToast("ボスが結界を再展開！"); 
                    }

                    if (!this.isInvincible && this.hitStun <= 0) {
                        if (Math.random() < 0.05) { this.vx = (Math.random()-0.5)*this.speed; this.vy = (Math.random()-0.5)*this.speed; }
                        this.attackCooldown -= dt;
                        if (this.attackCooldown <= 0 && dist < 350) {
                            this.attackCooldown = 1.0 + Math.random() * 0.5;
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, 250, this.color));
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle + 0.3, 250, this.color));
                            enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle - 0.3, 250, this.color));
                            if (Math.random() < 0.3) {
                                for(let i=0; i<8; i++) enemyProjectiles.push(new EnemyProjectile(this.x, this.y, (Math.PI/4)*i, 150, this.color));
                            }
                        }
                    }
                    this.x += this.vx * dt; this.y += this.vy * dt;
                }
                else {
                    if (dist < 300) { this.vx = Math.cos(angle)*this.speed; this.vy = Math.sin(angle)*this.speed; } else { this.vx = 0; this.vy = 0; }
                    this.x += this.vx * dt; this.y += this.vy * dt;
                    if (this.canShoot && this.hitStun <= 0) {
                        this.attackCooldown -= dt;
                        if (this.attackCooldown <= 0 && dist < 250) { this.attackCooldown = 2.0; enemyProjectiles.push(new EnemyProjectile(this.x, this.y, angle, 200, this.color)); }
                    }
                }
            }

            render(ctx) {
                if (this.isDead) {
                    if (this.respawnTimer > 0 && this.respawnTimer <= 3.0) {
                        ctx.save(); ctx.translate(this.spawnX, this.spawnY);
                        ctx.strokeStyle = `rgba(239, 68, 68, ${(3.0 - this.respawnTimer)/3.0})`;
                        ctx.lineWidth = 2; ctx.rotate(Date.now()*0.005);
                        ctx.beginPath(); ctx.arc(0, 0, this.radius * 1.5, 0, Math.PI*2); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(0, -this.radius*1.2); ctx.lineTo(this.radius*1.0, this.radius*0.6); ctx.lineTo(-this.radius*1.0, this.radius*0.6); ctx.closePath(); ctx.stroke();
                        ctx.beginPath(); ctx.moveTo(0, this.radius*1.2); ctx.lineTo(this.radius*1.0, -this.radius*0.6); ctx.lineTo(-this.radius*1.0, -this.radius*0.6); ctx.closePath(); ctx.stroke();
                        ctx.restore();
                    }
                    return;
                }

                if (this.type === 'slime' && imgSlime.complete && imgSlime.naturalWidth > 0) {
                    ctx.save(); ctx.translate(this.x, this.y);
                    if (this.state === 'prepare_attack') ctx.translate((Math.random()-0.5)*4, (Math.random()-0.5)*4);
                    ctx.drawImage(imgSlime, -this.radius*1.3, -this.radius*1.3, this.radius*2.6, this.radius*2.6);
                    ctx.restore();
                } else {
                    ctx.fillStyle = this.hitStun > 0 ? '#ffffff' : this.color; 
                    ctx.shadowColor = this.color; ctx.shadowBlur = 10;
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.radius, 0, Math.PI*2); ctx.fill(); ctx.shadowBlur = 0;
                }
                
                if (this.isInvincible) {
                    ctx.beginPath(); ctx.arc(this.x, this.y, this.barrierRadius, 0, Math.PI * 2); ctx.strokeStyle = 'rgba(56, 189, 248, 0.8)'; ctx.lineWidth = 3; ctx.stroke();
                    ctx.fillStyle = 'rgba(56, 189, 248, 0.15)'; ctx.fill();
                }
            }
        }"""

pattern_class = r"class Enemy \{[\s\S]*?\}\s*class EnemyProjectile"
new_content = re.sub(pattern_class, enemy_class + "\n\n        class EnemyProjectile", content)

pattern_update = r"enemies\.forEach\(e => \{[\s\S]*?if \(e\.type === 'boss'\) \{[\s\S]*?\}\s*\}\);"
new_content = re.sub(pattern_update, "enemies.forEach(e => e.update(dt));", new_content)

pattern_render = r"enemies\.forEach\(e => \{[\s\S]*?if \(!e\.isAlive\) return;[\s\S]*?ctx\.fillStyle = 'rgba\(56, 189, 248, 0\.15\)'; ctx\.fill\(\);\s*\}\s*\}\);"
new_content = re.sub(pattern_render, "enemies.forEach(e => e.render(ctx));", new_content)

# applyDamageToEnemy の変更
pattern_damage = r"function applyDamageToEnemy\(enemy, damageStr\) \{[\s\S]*?if \(enemy\.hp <= 0\) \{[\s\S]*?enemy\.isAlive = false;"
replacement_damage = r"""function applyDamageToEnemy(enemy, damageStr) {
            enemy.hitStun = 0.5; enemy.hp -= Math.max(1, damageStr);
            const ang = Math.atan2(enemy.y - player.y, enemy.x - player.x);
            enemy.vx = Math.cos(ang) * 300; enemy.vy = Math.sin(ang) * 300;

            if (enemy.hp <= 0) {
                enemy.isDead = true; enemy.respawnTimer = 15.0;"""
new_content = re.sub(pattern_damage, replacement_damage, new_content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Enemy refactor Done!')
