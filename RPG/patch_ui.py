import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. UIのHTMLを追加
ui_html = '''
    <!-- クエストボード UI -->
    <div id="questBoardOverlay" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 600px; background: rgba(20, 15, 10, 0.95); border: 2px solid #9d4edd; border-radius: 15px; padding: 20px; z-index: 1000; color: #fff; text-align: center; font-family: 'Noto Sans JP', sans-serif;">
        <h2 style="color: #4facfe; margin-bottom: 20px;">📜 ギルド クエストボード</h2>
        <div id="questList" style="text-align: left; margin-bottom: 20px; background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px;">
            <!-- クエスト内容が入る -->
        </div>
        <button onclick="document.getElementById('questBoardOverlay').style.display='none'; player.state = PlayerState.IDLE;" style="padding: 10px 20px; background: #e63946; color: white; border: none; border-radius: 5px; cursor: pointer;">閉じる</button>
    </div>

    <!-- 鍛冶屋 UI -->
    <div id="forgeOverlay" style="display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; background: rgba(20, 15, 10, 0.95); border: 2px solid #eab308; border-radius: 15px; padding: 20px; z-index: 1000; color: #fff; text-align: center; font-family: 'Noto Sans JP', sans-serif;">
        <h2 style="color: #eab308; margin-bottom: 20px;">🔨 鍛冶屋</h2>
        <div id="forgeStatus" style="margin-bottom: 20px; background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px;">
            <!-- ステータスが入る -->
        </div>
        <button id="btnUpgrade" style="padding: 10px 20px; background: #4ade80; color: #000; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px; font-weight: bold;">強化する</button>
        <button onclick="document.getElementById('forgeOverlay').style.display='none'; player.state = PlayerState.IDLE;" style="padding: 10px 20px; background: #e63946; color: white; border: none; border-radius: 5px; cursor: pointer;">立ち去る</button>
    </div>
'''

if 'id="questBoardOverlay"' not in html:
    html = html.replace('</body>', ui_html + '\n</body>')

# 2. JavaScriptの triggerInteract を書き換え
js_logic = '''
        if (typeof currentSceneId !== "undefined" && currentSceneId === 'guild' && player.y < 10 * TILE_SIZE) {
            player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
            const qb = document.getElementById('questBoardOverlay');
            const ql = document.getElementById('questList');
            qb.style.display = 'block';
            
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
                ql.innerHTML = "<h3 style='color:#4ade80'>新規クエストを受注しました！</h3><br>目的: " + player.activeQuest.name + "<br>報酬: " + player.activeQuest.reward + "G";
            } else {
                let isComplete = false;
                if (player.activeQuest.target === '鉄くず' && player.inventory['鉄くず'] >= player.activeQuest.req) {
                    player.inventory['鉄くず'] -= player.activeQuest.req;
                    isComplete = true;
                } else if (player.activeQuest.target !== '鉄くず' && player.questProgress >= player.activeQuest.req) {
                    isComplete = true;
                }
                
                if (isComplete) {
                    player.gold += player.activeQuest.reward;
                    ql.innerHTML = "<h3 style='color:#fcd34d'>クエスト報告完了！</h3><br>報酬 " + player.activeQuest.reward + "G を獲得しました！";
                    player.activeQuest = null; player.questProgress = 0;
                } else {
                    ql.innerHTML = "<h3 style='color:#fff'>現在進行中のクエスト</h3><br>目的: " + player.activeQuest.name + "<br>進行度: " + player.questProgress + " / " + player.activeQuest.req;
                }
            }
            return;
        }

        // 鍛冶屋の座標をより入り口付近 (x:38-42, y:20-25) などに近づける。ここでは距離を広めにとる
        if (typeof currentSceneId !== "undefined" && currentSceneId === 'city' && player.y > 10 * TILE_SIZE && player.y < 25 * TILE_SIZE && player.x > 50 * TILE_SIZE) {
            player.state = PlayerState.DIALOGUE; player.vx = 0; player.vy = 0;
            const fo = document.getElementById('forgeOverlay');
            const fs = document.getElementById('forgeStatus');
            const btn = document.getElementById('btnUpgrade');
            fo.style.display = 'block';
            
            const updateForgeUI = () => {
                let cost = player.weaponLevel * 100;
                fs.innerHTML = "現在の武器Lv: " + player.weaponLevel + "<br>現在の防具Lv: " + player.armorLevel + "<br><br>【強化に必要な素材】<br>鉄くず: 1個 (所持: " + (player.inventory['鉄くず']||0) + ")<br>ゴールド: " + cost + "G (所持: " + player.gold + "G)";
                
                btn.onclick = () => {
                    if ((player.inventory['鉄くず']||0) >= 1 && player.gold >= cost) {
                        player.inventory['鉄くず']--; player.gold -= cost;
                        player.weaponLevel++; player.armorLevel++; player.atk += 2; player.def += 1;
                        updateForgeUI();
                    } else {
                        fs.innerHTML += "<br><span style='color:#e63946'>素材またはゴールドが足りません！</span>";
                    }
                };
            };
            updateForgeUI();
            return;
        }
'''

# 既存のクエスト・鍛冶屋ロジックを置換する
# "if (typeof currentSceneId !== "undefined" && currentSceneId === 'guild' && player.y < 5 * TILE_SIZE) {"
# から始まるブロックを置換
html = re.sub(r'if \(typeof currentSceneId !== "undefined" && currentSceneId === \'guild\'[\s\S]*?return;\n        \}', js_logic.strip(), html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('UI and Logic replaced successfully.')
