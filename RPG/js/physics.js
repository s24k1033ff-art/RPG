// physics.js

function getTileAt(x, y) {
    const col = Math.floor(x / TILE_SIZE);
    const row = Math.floor(y / TILE_SIZE);
    if (col < 0 || col >= MAP_COLS || row < 0 || row >= MAP_ROWS) return 1; // 画面外は壁
    if (!map[row] || map[row][col] === undefined) return 1; // フェイルセーフ
    return map[row][col];
}

function resolveSafetyCollisions() {
    // プレイヤーの壁抜け防止（より確実な4方向押し出し）
    const dirs = [
        {x: 0, y: -1}, // 上
        {x: 0, y: 1},  // 下
        {x: -1, y: 0}, // 左
        {x: 1, y: 0}   // 右
    ];
    
    // タイル 1:壁, 4:青扉, 7:赤扉, 8:緑扉, 9:紫扉, 11: 魔法の壁など
    const solidTiles = [1, 4, 7, 8, 9, 11];

    dirs.forEach(dir => {
        const cx = player.x + dir.x * (COLLISION_RADIUS + SAFE_MARGIN);
        const cy = player.y + dir.y * (COLLISION_RADIUS + SAFE_MARGIN);
        const tile = getTileAt(cx, cy);
        
        if (solidTiles.includes(tile)) {
            // 壁にめり込んでいる場合、押し出す
            if (dir.x !== 0) {
                const wallX = Math.floor(cx / TILE_SIZE) * TILE_SIZE + (dir.x > 0 ? 0 : TILE_SIZE);
                player.x = wallX - dir.x * (COLLISION_RADIUS + SAFE_MARGIN + 0.1);
            }
            if (dir.y !== 0) {
                const wallY = Math.floor(cy / TILE_SIZE) * TILE_SIZE + (dir.y > 0 ? 0 : TILE_SIZE);
                player.y = wallY - dir.y * (COLLISION_RADIUS + SAFE_MARGIN + 0.1);
            }
        }
    });

    // マップ外に出ないようにする
    player.x = Math.max(COLLISION_RADIUS, Math.min(player.x, MAP_COLS * TILE_SIZE - COLLISION_RADIUS));
    player.y = Math.max(COLLISION_RADIUS, Math.min(player.y, MAP_ROWS * TILE_SIZE - COLLISION_RADIUS));
}
