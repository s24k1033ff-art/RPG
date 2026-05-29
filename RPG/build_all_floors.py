import re

W, H = 80, 80

def make_grid(w=80, h=80):
    return [['1' for _ in range(w)] for _ in range(h)]

def draw_room(grid, cx, cy, w, h, tile='0', gw=80, gh=80):
    for y in range(cy-h//2, cy+h//2):
        for x in range(cx-w//2, cx+w//2):
            if 0 <= y < gh and 0 <= x < gw:
                grid[y][x] = tile

def tiles_to_js(grid):
    lines = []
    for row in grid:
        lines.append('                    "' + ''.join(row) + '"')
    return ',\n'.join(lines)

# ========== FLOOR 2: 巨石と機構の試練 ==========
def build_f2():
    g = make_grid(60, 60)
    # [1] 転移門 (30, 55)
    draw_room(g, 30, 55, 10, 8, gw=60, gh=60)
    # 通路: 転移門 -> 仕分け部屋
    draw_room(g, 30, 48, 4, 10, gw=60, gh=60)
    # [2] 巨石の仕分け部屋 (30, 40)
    draw_room(g, 30, 40, 16, 12, gw=60, gh=60)
    # 西への通路 -> 射撃回廊
    draw_room(g, 18, 40, 12, 4, gw=60, gh=60)
    # [3] 西の射撃回廊 (10, 30)
    draw_room(g, 10, 30, 16, 16, gw=60, gh=60)
    draw_room(g, 10, 38, 4, 8, gw=60, gh=60)
    # 東への通路 -> 崩落通路
    draw_room(g, 42, 40, 12, 4, gw=60, gh=60)
    # [4] 東の崩落通路 (50, 30)
    draw_room(g, 50, 30, 16, 16, gw=60, gh=60)
    draw_room(g, 50, 38, 4, 8, gw=60, gh=60)
    # [5] 吹き抜けの大空洞 (中央上部)
    draw_room(g, 30, 20, 20, 12, gw=60, gh=60)
    # 西から空洞へ
    draw_room(g, 15, 22, 10, 4, gw=60, gh=60)
    # 東から空洞へ
    draw_room(g, 45, 22, 10, 4, gw=60, gh=60)
    # 空洞の中央に穴（tile 2）
    draw_room(g, 30, 18, 8, 4, '2', gw=60, gh=60)
    # [6] ボス部屋 (30, 8)
    draw_room(g, 30, 8, 20, 12, gw=60, gh=60)
    draw_room(g, 30, 15, 4, 4, gw=60, gh=60)
    # ボス部屋へのゲート（穴を埋めないと通れない）
    for x in range(28, 32):
        g[14][x] = '4'  # 青扉で封鎖

    return {
        'id': 'dungeon_f2', 'w': 60, 'h': 60,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f2',
        'portals': "{ c: 30, r: 55, dest: 'dungeon_f1', sc: 40, sr: 8 }",
        'enemies': """
                    { c: 10, r: 28, type: 'skeleton' }, { c: 12, r: 32, type: 'skeleton' },
                    { c: 48, r: 28, type: 'slime' }, { c: 52, r: 30, type: 'slime' }, { c: 50, r: 32, type: 'slime' },
                    { c: 25, r: 20, type: 'bat' }, { c: 35, r: 20, type: 'bat' },
                    { c: 30, r: 8, type: 'boss' }""",
        'chests': """
                    { c: 8, r: 26, opened: false, keyId: 'start', color: '#38bdf8' },
                    { c: 52, r: 26, opened: false, keyId: 'gold', color: '#fbbf24' }""",
        'spawn': '30, 55'
    }

# ========== FLOOR 3: 機巧と焦燥の回廊 ==========
def build_f3():
    g = make_grid(60, 60)
    # [1] 転移門
    draw_room(g, 30, 55, 10, 8, gw=60, gh=60)
    draw_room(g, 30, 48, 4, 10, gw=60, gh=60)
    # 分岐ハブ
    draw_room(g, 30, 42, 16, 8, gw=60, gh=60)
    # [2] 西: 焦燥の回廊
    draw_room(g, 12, 35, 16, 20, gw=60, gh=60)
    draw_room(g, 20, 42, 8, 4, gw=60, gh=60)
    # コンベアタイル（tile 'a'）を西回廊の一部に
    for y in range(28, 42):
        for x in range(6, 10):
            g[y][x] = 'a'
    # [3] 東: パニックルーム
    draw_room(g, 48, 35, 16, 20, gw=60, gh=60)
    draw_room(g, 40, 42, 8, 4, gw=60, gh=60)
    # トゲ床（tile 3）を中央に
    draw_room(g, 48, 35, 6, 6, '3', gw=60, gh=60)
    # [4] 逆流の試練（中央突破）
    draw_room(g, 30, 22, 12, 10, gw=60, gh=60)
    draw_room(g, 30, 30, 4, 12, gw=60, gh=60)
    # 西→中央
    draw_room(g, 18, 25, 12, 4, gw=60, gh=60)
    # 東→中央
    draw_room(g, 42, 25, 12, 4, gw=60, gh=60)
    # コンベア逆流（tile 'a'）
    for y in range(20, 26):
        for x in range(26, 34):
            g[y][x] = 'a'
    # [5] ボス部屋
    draw_room(g, 30, 8, 20, 14, gw=60, gh=60)
    draw_room(g, 30, 16, 4, 4, gw=60, gh=60)
    # ボス扉
    for x in range(28, 32):
        g[15][x] = '4'

    return {
        'id': 'dungeon_f3', 'w': 60, 'h': 60,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f3',
        'portals': "{ c: 30, r: 55, dest: 'dungeon_f2', sc: 30, sr: 8 }",
        'enemies': """
                    { c: 10, r: 30, type: 'bat' }, { c: 14, r: 32, type: 'bat' },
                    { c: 46, r: 30, type: 'slime' }, { c: 48, r: 34, type: 'slime' }, { c: 50, r: 32, type: 'slime' },
                    { c: 28, r: 22, type: 'skeleton' }, { c: 32, r: 22, type: 'skeleton' },
                    { c: 30, r: 8, type: 'boss' }""",
        'chests': "{ c: 10, r: 28, opened: false, keyId: 'start', color: '#38bdf8' }",
        'spawn': '30, 55'
    }

# ========== FLOOR 4: 閉ざされた観測所 ==========
def build_f4():
    g = make_grid(50, 50)
    W4, H4 = 50, 50
    # [A] 転移門
    draw_room(g, 10, 45, 10, 8, gw=W4, gh=H4)
    # [B] 最初の試練部屋
    draw_room(g, 10, 30, 14, 14, gw=W4, gh=H4)
    # ワープタイル (tile 'w')
    g[45][10] = 'w'  # A->B warp
    g[30][10] = 'w'  # B arrival
    # [C] 錯綜の大広間（ハブ）
    draw_room(g, 30, 25, 18, 18, gw=W4, gh=H4)
    g[25][22] = 'w'  # B->C warp
    g[25][25] = 'w'  # trap warp (wrong)
    g[25][28] = 'w'  # correct -> D
    g[25][31] = 'w'  # trap warp (wrong)
    g[25][34] = 'w'  # treasure room
    # [D] 正解の小部屋
    draw_room(g, 40, 10, 12, 10, gw=W4, gh=H4)
    g[10][40] = 'w'  # D->E warp
    # [E] ボス部屋
    draw_room(g, 25, 5, 20, 8, gw=W4, gh=H4)
    # [F] トラップ部屋
    draw_room(g, 10, 10, 12, 10, gw=W4, gh=H4)
    draw_room(g, 10, 10, 6, 6, '3', gw=W4, gh=H4)  # トゲ
    g[10][10] = 'w'  # back to start
    # [G] 宝物庫
    draw_room(g, 40, 40, 10, 10, gw=W4, gh=H4)
    g[40][40] = 'w'  # back to C

    return {
        'id': 'dungeon_f4', 'w': W4, 'h': H4,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f4',
        'portals': "{ c: 10, r: 45, dest: 'dungeon_f3', sc: 30, sr: 8 }",
        'enemies': """
                    { c: 10, r: 28, type: 'slime' }, { c: 12, r: 32, type: 'slime' },
                    { c: 28, r: 22, type: 'bat' }, { c: 32, r: 24, type: 'bat' },
                    { c: 10, r: 8, type: 'skeleton' }, { c: 12, r: 12, type: 'skeleton' },
                    { c: 25, r: 5, type: 'boss' }""",
        'chests': """
                    { c: 42, r: 40, opened: false, keyId: 'gold', color: '#fbbf24' },
                    { c: 40, r: 8, opened: false, keyId: 'gold', color: '#fbbf24' }""",
        'spawn': '10, 45'
    }

# ========== FLOOR 5: 深淵の共鳴炉 ==========
def build_f5():
    g = make_grid(60, 60)
    # [1] 転移門
    draw_room(g, 30, 55, 10, 8, gw=60, gh=60)
    draw_room(g, 30, 48, 4, 10, gw=60, gh=60)
    # [2] 中央共鳴室 (HUB)
    draw_room(g, 30, 38, 20, 16, gw=60, gh=60)
    # 北の障壁（ボス部屋へ）
    for x in range(26, 34):
        g[30][x] = '4'
    # [3] 東のコンベア回廊
    draw_room(g, 48, 38, 16, 14, gw=60, gh=60)
    draw_room(g, 38, 38, 8, 4, gw=60, gh=60)
    for y in range(34, 42):
        for x in range(42, 46):
            g[y][x] = 'a'
    # [4] 西の暗黒ワープ区
    draw_room(g, 12, 38, 16, 14, gw=60, gh=60)
    draw_room(g, 22, 38, 8, 4, gw=60, gh=60)
    # [5] 南の隠し部屋
    draw_room(g, 30, 56, 8, 6, gw=60, gh=60)
    # [6] ボス部屋
    draw_room(g, 30, 15, 22, 18, gw=60, gh=60)
    draw_room(g, 30, 27, 4, 8, gw=60, gh=60)

    return {
        'id': 'dungeon_f5', 'w': 60, 'h': 60,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f5',
        'portals': "{ c: 30, r: 55, dest: 'dungeon_f4', sc: 25, sr: 5 }",
        'enemies': """
                    { c: 46, r: 36, type: 'skeleton' }, { c: 50, r: 40, type: 'skeleton' },
                    { c: 10, r: 36, type: 'bat' }, { c: 14, r: 40, type: 'bat' },
                    { c: 28, r: 38, type: 'slime' }, { c: 32, r: 38, type: 'slime' },
                    { c: 30, r: 15, type: 'boss' }""",
        'chests': """
                    { c: 50, r: 34, opened: false, keyId: 'start', color: '#38bdf8' },
                    { c: 10, r: 34, opened: false, keyId: 'forest', color: '#10b981' },
                    { c: 30, r: 57, opened: false, keyId: 'gold', color: '#fbbf24' }""",
        'spawn': '30, 55'
    }

# ========== FLOOR 6: 浸食された緑廊 ==========
def build_f6():
    g = make_grid(60, 50)
    W6, H6 = 60, 50
    # [1] 上層: 転移門 (スタート)
    draw_room(g, 50, 10, 14, 14, gw=W6, gh=H6)
    # 上層通路
    draw_room(g, 38, 10, 16, 6, gw=W6, gh=H6)
    # [2] 下層: 浸水の回廊
    draw_room(g, 20, 30, 24, 16, gw=W6, gh=H6)
    # 崖（一方通行段差）tile '2'
    for x in range(35, 45):
        g[18][x] = '2'
    # [3] 静寂の雑貨店 (Safe Zone)
    draw_room(g, 48, 35, 12, 10, gw=W6, gh=H6)
    draw_room(g, 40, 35, 8, 4, gw=W6, gh=H6)
    # [4] 次階層への転移門（上層）
    draw_room(g, 10, 8, 12, 10, gw=W6, gh=H6)
    # ツタ（tile 'v'）
    g[22][20] = 'v'
    g[22][30] = 'v'
    # 上層通路 -> 次階層
    draw_room(g, 18, 10, 12, 6, gw=W6, gh=H6)

    return {
        'id': 'dungeon_f6', 'w': W6, 'h': H6,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f6',
        'portals': "{ c: 50, r: 10, dest: 'dungeon_f5', sc: 30, sr: 15 }",
        'npcs': "{ c: 48, r: 35, id: 'shopkeeper', name: 'エルザ（雑貨店）' }",
        'enemies': """
                    { c: 18, r: 28, type: 'slime' }, { c: 22, r: 32, type: 'slime' },
                    { c: 28, r: 30, type: 'bat' }, { c: 15, r: 34, type: 'skeleton' },
                    { c: 10, r: 8, type: 'mini_boss' }""",
        'chests': "{ c: 15, r: 36, opened: false, keyId: 'gold', color: '#fbbf24' }",
        'spawn': '50, 10'
    }

# ========== FLOOR 7: 木漏れ日と胞子の迷宮 ==========
def build_f7():
    g = make_grid(60, 50)
    W7, H7 = 60, 50
    # [1] 転移門（上層）
    draw_room(g, 50, 10, 12, 12, gw=W7, gh=H7)
    # 崖（飛び降り）
    for x in range(38, 50):
        g[16][x] = '2'
    # [2] 下層: 胞子の海
    draw_room(g, 30, 30, 30, 20, gw=W7, gh=H7)
    # 毒エリア（tile '3' をスパイク代用）
    draw_room(g, 30, 32, 20, 12, '3', gw=W7, gh=H7)
    # [3] 浄化の木漏れ日（安全地帯 - 下層内）
    draw_room(g, 20, 32, 6, 6, '0', gw=W7, gh=H7)
    draw_room(g, 40, 32, 6, 6, '0', gw=W7, gh=H7)
    # ツタ
    g[22][20] = 'v'
    g[22][40] = 'v'
    # 上層通路
    draw_room(g, 30, 8, 30, 8, gw=W7, gh=H7)
    # [4] 次階層への転移門（上層最奥）
    draw_room(g, 10, 8, 12, 10, gw=W7, gh=H7)

    return {
        'id': 'dungeon_f7', 'w': W7, 'h': H7,
        'tiles': tiles_to_js(g),
        'theme': 'dungeon_f7',
        'portals': "{ c: 50, r: 10, dest: 'dungeon_f6', sc: 10, sr: 8 }",
        'enemies': """
                    { c: 25, r: 30, type: 'slime' }, { c: 35, r: 30, type: 'slime' },
                    { c: 30, r: 28, type: 'bat' }, { c: 22, r: 34, type: 'bat' },
                    { c: 38, r: 34, type: 'skeleton' },
                    { c: 10, r: 8, type: 'mini_boss' }""",
        'chests': """
                    { c: 30, r: 35, opened: false, keyId: 'gold', color: '#fbbf24' },
                    { c: 10, r: 6, opened: false, keyId: 'gold', color: '#fbbf24' }""",
        'spawn': '50, 10'
    }

# ========== 全階層のJSコードを生成 ==========
floors = [build_f2(), build_f3(), build_f4(), build_f5(), build_f6(), build_f7()]

# 新テーマ定義
new_themes = """
            dungeon_f2: { name: "第2階層：巨石と機構の試練", floor: '#0f172a', wall: '#1e293b', border: '#f59e0b', pit: '#020617', spike: '#ef4444', npc: '#38bdf8' },
            dungeon_f3: { name: "第3階層：機巧と焦燥の回廊", floor: '#0c0a09', wall: '#292524', border: '#22d3ee', pit: '#020617', spike: '#ef4444', npc: '#38bdf8' },
            dungeon_f4: { name: "第4階層：閉ざされた観測所", floor: '#030712', wall: '#111827', border: '#6366f1', pit: '#000', spike: '#ef4444', npc: '#818cf8' },
            dungeon_f5: { name: "第5階層：深淵の共鳴炉", floor: '#0c0a09', wall: '#1c1917', border: '#f43f5e', pit: '#020617', spike: '#ef4444', npc: '#fb7185' },
            dungeon_f6: { name: "第6階層：浸食された緑廊", floor: '#052e16', wall: '#14532d', border: '#4ade80', pit: '#022c22', spike: '#ef4444', npc: '#86efac' },
            dungeon_f7: { name: "第7階層：木漏れ日と胞子の迷宮", floor: '#1a2e05', wall: '#365314', border: '#a3e635', pit: '#1a2e05', spike: '#c084fc', npc: '#bef264' }"""

# 各フロアのsceneDataエントリを生成
scene_entries = []
for f in floors:
    npcs_str = f.get('npcs', '')
    npcs_arr = f'[\n                    {npcs_str}\n                ]' if npcs_str else '[]'
    entry = f"""
            '{f['id']}': {{
                width: {f['w']}, height: {f['h']},
                tiles: [
{f['tiles']}
                ],
                portals: [
                    {f['portals']}
                ],
                npcs: {npcs_arr},
                enemies: [{f['enemies']}
                ],
                chests: [{f['chests']}
                ],
                getTheme: () => themes.{f['theme']}
            }}"""
    scene_entries.append(entry)

# HTMLファイルを読み込み
with open('preview_demo.html', 'r', encoding='utf-8') as file:
    content = file.read()

# 1. テーマに新階層を追加
old_themes_end = "crystal: { name: \"魔導クリスタル鉱脈\", floor: '#1e1b4b', wall: '#312e81', border: '#c084fc', pit: '#020617', spike: '#8b5cf6', npc: '#c084fc' }"
new_themes_block = old_themes_end + "," + new_themes
content = content.replace(old_themes_end, new_themes_block)

# 2. dungeon_f2のプレースホルダーを実際のデータに置換し、F3-F7を追加
old_f2 = """'dungeon_f2': {
                width: 40, height: 40,
                tiles: Array(40).fill("1".repeat(40)),
                portals: [{ c: 20, r: 38, dest: 'dungeon_f1', sc: 40, r: 8 }],
                npcs: [], enemies: [], chests: [],
                getTheme: () => themes.crystal
            }"""

new_scenes = ','.join(scene_entries)
content = content.replace(old_f2, new_scenes.lstrip(',').strip())

# 3. ボス討伐時のポータル遷移先を全階層分に拡張
old_portal_logic = """if (currentSceneId === 'dungeon_f1') { nextDest = 'dungeon_f2'; nextSc = 2; nextSr = 3; }
                    else if (currentSceneId === 'dungeon_f2') { nextDest = 'city'; }"""
new_portal_logic = """if (currentSceneId === 'dungeon_f1') { nextDest = 'dungeon_f2'; nextSc = 30; nextSr = 55; }
                    else if (currentSceneId === 'dungeon_f2') { nextDest = 'dungeon_f3'; nextSc = 30; nextSr = 55; }
                    else if (currentSceneId === 'dungeon_f3') { nextDest = 'dungeon_f4'; nextSc = 10; nextSr = 45; }
                    else if (currentSceneId === 'dungeon_f4') { nextDest = 'dungeon_f5'; nextSc = 30; nextSr = 55; }
                    else if (currentSceneId === 'dungeon_f5') { nextDest = 'dungeon_f6'; nextSc = 50; nextSr = 10; }
                    else if (currentSceneId === 'dungeon_f6') { nextDest = 'dungeon_f7'; nextSc = 50; nextSr = 10; }
                    else if (currentSceneId === 'dungeon_f7') { nextDest = 'city'; }"""
content = content.replace(old_portal_logic, new_portal_logic)

with open('preview_demo.html', 'w', encoding='utf-8') as file:
    file.write(content)

print(f"All {len(floors)} floors built and applied successfully!")
print("Floors: F2-F7 added to sceneData")
print("Themes: 6 new biome themes added")
print("Portal chain: F1->F2->F3->F4->F5->F6->F7->city")
