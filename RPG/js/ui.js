// ui.js

function updateHUD() {
    const soul = souls[player.currentSoulId];
    
    // 画像の更新
    document.getElementById('soulImage').src = soul.img;
    document.getElementById('charIcon').style.borderColor = soul.color;

    if (player.xp >= player.xpNeeded) {
        player.level++;
        player.xp -= player.xpNeeded;
        player.xpNeeded = Math.floor(player.xpNeeded * 1.5);
        soul.level = player.level;
        soul.maxHp += 10; soul.atk += 2; soul.def += 1;
        player.maxHp = soul.maxHp + player.foodBuffs.maxHp + player.memoryBonuses.maxHp;
        player.hp = player.maxHp;
        player.atk = soul.atk + player.foodBuffs.atk + (player.weaponLevel - 1) * 2;
        player.def = soul.def + player.foodBuffs.def + (player.armorLevel - 1) * 1;
        showToast(`レベルアップ！ ${soul.name} Lv.${player.level}`);
    }
    
    document.getElementById('hpText').textContent = `${Math.floor(player.hp)}/${player.maxHp}`;
    document.getElementById('hpFill').style.width = `${(player.hp / player.maxHp) * 100}%`;
    document.getElementById('mpText').textContent = `${Math.floor(player.mp)}/${player.maxMp}`;
    document.getElementById('mpFill').style.width = `${(player.mp / player.maxMp) * 100}%`;
    document.getElementById('xpText').textContent = `${soul.name} Lv.${player.level} (${Math.floor(player.xp)}/${player.xpNeeded})`;
    document.getElementById('xpFill').style.width = `${(player.xp / player.xpNeeded) * 100}%`;
    document.getElementById('goldText').textContent = `${player.gold}G`;

    const q = player.activeQuest;
    if (q) document.getElementById('questText').textContent = `クエスト: ${q.name} (${player.questProgress}/${q.req})`;
    else document.getElementById('questText').textContent = "クエスト: なし";
}

function openMenu() {
    if (player.state === PlayerState.DIALOGUE) return;
    player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
    document.getElementById('menuWep').textContent = player.weaponLevel;
    document.getElementById('menuArm').textContent = player.armorLevel;
    document.getElementById('menuBuffHp').textContent = player.foodBuffs.maxHp;
    document.getElementById('menuBuffAtk').textContent = player.foodBuffs.atk;
    document.getElementById('menuBuffDef').textContent = player.foodBuffs.def;
    document.getElementById('menuShards').textContent = player.memoryShards;
    
    const invList = document.getElementById('menuInvList');
    invList.innerHTML = '';
    for (const [item, count] of Object.entries(player.inventory)) {
        if (count > 0) {
            invList.innerHTML += `<li style="margin-bottom: 5px;">${item}: <span style="color:#fbbf24">${count}</span> 個</li>`;
        }
    }
    
    document.getElementById('menuOverlay').classList.add('show');
}

function closeMenu() {
    document.getElementById('menuOverlay').classList.remove('show');
    setTimeout(() => { player.state = PlayerState.IDLE; }, 100);
}

function showToast(msg, duration = 2000) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    document.getElementById('toastContainer').appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function openShop() {
    if (player.state === PlayerState.DIALOGUE) return;
    player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
    document.getElementById('shopOverlay').classList.add('show');
}
function closeShop() {
    document.getElementById('shopOverlay').classList.remove('show');
    setTimeout(() => { player.state = PlayerState.IDLE; }, 100);
}
function buyItem(type, price) {
    if (player.gold < price) { showToast("ゴールドが足りません！"); return; }
    player.gold -= price;
    if (type === 'potion') { player.hp = Math.min(player.maxHp, player.hp + 50); showToast("ポーションを使用しました"); }
    else if (type === 'ether') { player.mp = Math.min(player.maxMp, player.mp + 30); showToast("エーテルを使用しました"); }
    else if (type === 'bomb') { showToast("ボムは未実装です"); player.gold += price; }
    updateHUD();
}

// クラスチェンジ（ソウル・ドライブ）
function changeSoul(soulId) {
    player.currentSoulId = soulId;
    const s = souls[soulId];
    player.level = s.level; player.xp = s.xp; player.xpNeeded = s.xpNeeded;
    player.maxHp = s.maxHp + player.foodBuffs.maxHp + player.memoryBonuses.maxHp;
    player.maxMp = s.maxMp;
    player.atk = s.atk + player.foodBuffs.atk + (player.weaponLevel - 1) * 2;
    player.def = s.def + player.foodBuffs.def + (player.armorLevel - 1) * 1;
    player.spd = s.spd + player.foodBuffs.spd;
    player.hp = Math.min(player.hp, player.maxHp);
    player.mp = Math.min(player.mp, player.maxMp);
    showToast(`【ソウル・ドライブ】${s.name} に憑依しました！`);
    updateHUD();
}

function openCooking() {
    if (player.state === PlayerState.DIALOGUE) return;
    player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
    dialogueState = { 
        active: true, 
        lines: [
            "🍳 【酒場の女主人】",
            "あら、素材を持ってきたのね。料理してあげるわ。",
            "（魔物の肉と地下野菜を消費して、最大HPとATKが上昇しました！）"
        ], 
        lineIdx: 0, charIdx: 0, timer: 0 
    };
    if (player.inventory['魔物の肉'] > 0 && player.inventory['地下野菜'] > 0) {
        player.inventory['魔物の肉']--; player.inventory['地下野菜']--;
        player.foodBuffs.maxHp += 20; player.foodBuffs.atk += 3;
        player.maxHp += 20; player.atk += 3; player.hp += 20;
    } else {
        dialogueState.lines[2] = "（素材が足りないみたいね。『魔物の肉』と『地下野菜』を集めてきて！）";
    }
    document.getElementById('dialogueName').textContent = "酒場の女主人"; 
    document.getElementById('dialogueText').textContent = ""; 
    document.getElementById('dialogueOverlay').classList.add('show');
    updateHUD();
}

function openBlacksmith() {
    if (player.state === PlayerState.DIALOGUE) return;
    player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
    dialogueState = { 
        active: true, 
        lines: [
            "🔨 【鍛冶屋の親父】",
            `現在の武器Lv: ${player.weaponLevel} / 防具Lv: ${player.armorLevel}`,
            "強化には鉄くずとゴールドが必要だ。自動で強化しとくぜ！"
        ], 
        lineIdx: 0, charIdx: 0, timer: 0 
    };
    const cost = player.weaponLevel * 100;
    if (player.gold >= cost && player.inventory['鉄くず'] >= 1) {
        player.gold -= cost; player.inventory['鉄くず']--;
        player.weaponLevel++; player.armorLevel++;
        player.atk += 2; player.def += 1;
        dialogueState.lines.push(`チャキーン！ 強化成功だ！ (ATK+2, DEF+1)`);
    } else {
        dialogueState.lines.push(`素材（鉄くず 1個）とゴールド（${cost}G）が足りねえな。`);
    }
    document.getElementById('dialogueName').textContent = "鍛冶屋の親父"; 
    document.getElementById('dialogueText').textContent = ""; 
    document.getElementById('dialogueOverlay').classList.add('show');
    updateHUD();
}

function useMemoryShard() {
    if (player.memoryShards > 0) {
        player.memoryShards--;
        player.memoryBonuses.maxHp += 10;
        player.maxHp += 10; player.hp += 10;
        showToast("『記憶の欠片』を復元した！ かつての仲間の記憶がよみがえり、最大HPが+10された！", 4000);
        updateHUD();
    } else {
        showToast("『記憶の欠片』を持っていません。ボスの討伐や隠し宝箱から探しましょう。");
    }
}

function triggerInteract() {
    const adjTiles = [
        getTileAt(player.x, player.y), getTileAt(player.x, player.y - 18), getTileAt(player.x, player.y + 18), 
        getTileAt(player.x - 18, player.y), getTileAt(player.x + 18, player.y)
    ];

    if (adjTiles.includes(14)) { openShop(); return; } // 'e' SHOP
    if (adjTiles.includes(15)) { openBlacksmith(); return; } // 'f' FORGE
    if (adjTiles.includes(16)) { openCooking(); return; } // 'g' TAVERN (料理)

    // NPC
    const npc = currentScene.npcs && currentScene.npcs.find(n => Math.hypot((n.c+0.5)*TILE_SIZE - player.x, (n.r+0.5)*TILE_SIZE - player.y) < 50);
    if (npc) {
        player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
        let lines = ["..."];
        if (npc.id === 'guide') lines = ["🤕 おい、大丈夫か？", "ここは迷宮都市アビス・エッジ。", "記憶がない？ 『ソウル・ドライブ』を使って戦うんだ。"];
        else if (npc.id === 'guildmaster') {
            lines = ["🍻 よく来たな。素材はここで換金してやる。"];
            let earned = 0;
            ['スライムの粘液', '鉄くず', '風の結晶', 'アビスコア'].forEach(item => {
                const count = player.inventory[item] || 0;
                if (count > 0) {
                    const price = item === 'スライムの粘液' ? 10 : (item === '風の結晶' ? 25 : (item === '鉄くず' ? 50 : 500));
                    earned += price * count; player.inventory[item] = 0;
                }
            });
            if (earned > 0) { player.gold += earned; lines.push(`素材を売却して ${earned}G 手に入れた！`); }
        }
        dialogueState = { active: true, lines, lineIdx: 0, charIdx: 0, timer: 0 };
        document.getElementById('dialogueName').textContent = npc.name; document.getElementById('dialogueText').textContent = ""; 
        document.getElementById('dialogueOverlay').classList.add('show');
        return;
    }

    // クエストボード
    if (adjTiles.includes(17) || (currentSceneId === 'guild' && player.y < 3 * TILE_SIZE)) {
        player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
        if (!player.activeQuest) {
            const quests = [
                { id: 1, name: 'スライム討伐', target: 'slime', req: 5, reward: 100 },
                { id: 2, name: 'コウモリの脅威', target: 'bat', req: 8, reward: 150 },
                { id: 4, name: 'ボス討伐', target: 'boss', req: 1, reward: 1000 }
            ];
            const q = quests[Math.floor(Math.random() * quests.length)];
            player.activeQuest = q; player.questProgress = 0;
            dialogueState = { active: true, lines: [`📜 【クエストボード】\n★ 『${q.name}』を受注しました！`], lineIdx: 0, charIdx: 0, timer: 0 };
        } else if (player.questProgress >= player.activeQuest.req) {
            player.gold += player.activeQuest.reward;
            dialogueState = { active: true, lines: [`📜 【クエストボード】\n★ 報告完了！ 報酬の【${player.activeQuest.reward}G】を獲得！`], lineIdx: 0, charIdx: 0, timer: 0 };
            player.activeQuest = null; player.questProgress = 0;
        } else {
            dialogueState = { active: true, lines: [`📜 【クエストボード】\n★ 進行度: ${player.questProgress}/${player.activeQuest.req}`], lineIdx: 0, charIdx: 0, timer: 0 };
        }
        document.getElementById('dialogueName').textContent = "クエストボード"; document.getElementById('dialogueText').textContent = ""; 
        document.getElementById('dialogueOverlay').classList.add('show');
        return;
    }
}

