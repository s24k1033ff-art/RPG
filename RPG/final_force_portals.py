import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 強制ポータル（update関数内に差し込む）
force_portals = '''
        if (typeof currentSceneId !== 'undefined' && player) {
            if (currentSceneId === 'guild' && player.y > 28 * TILE_SIZE) {
                loadScene('city'); player.x = 40 * TILE_SIZE; player.y = 12 * TILE_SIZE;
            } else if (currentSceneId === 'city' && player.y < 12 * TILE_SIZE && player.x > 38 * TILE_SIZE && player.x < 42 * TILE_SIZE) {
                loadScene('guild'); player.x = 40 * TILE_SIZE; player.y = 25 * TILE_SIZE;
            } else if (currentSceneId === 'city' && player.y > 50 * TILE_SIZE) {
                loadScene('dungeon_f1'); player.x = 40 * TILE_SIZE; player.y = 74 * TILE_SIZE;
            } else if (currentSceneId.startsWith('dungeon') && player.y > 75 * TILE_SIZE) {
                loadScene('city'); player.x = 40 * TILE_SIZE; player.y = 30 * TILE_SIZE;
            }
        }
'''
html = html.replace('function update(time) {', 'function update(time) {\n' + force_portals)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Final forced portals added.')
