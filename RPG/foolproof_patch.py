import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ギルドのポータルが追加されなかった場合の保険
if 'dest: \'city\', sc: 40, sr: 12' not in html:
    html = re.sub(r'\'guild\': \{[\s\S]*?portals: \[[\s\S]*?\]', r"'guild': { type: 'city', portals: [\n                    { c: 40, r: 28, dest: 'city', sc: 40, sr: 12 },\n                ]", html)

# 鍛冶屋とクエストボードの追加
quest_board = '''
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

html = re.sub(r'(function triggerInteract\(\) \{)', r'\1\n' + quest_board, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Patched successfully!')
