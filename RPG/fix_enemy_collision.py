import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Enemy クラスに move メソッドを追加
move_method = """            move(dt) {
                let nx = this.x + this.vx * dt;
                let ny = this.y + this.vy * dt;
                // コウモリ以外は壁に引っかかる（コウモリも壁は越えられない）
                const tile = getTileAt(nx, ny);
                if (tile === 1 || tile === 4 || tile === 8 || tile === 9 || tile === 7 || tile === 3) {
                    const tx = getTileAt(nx, this.y);
                    if (tx === 1 || tx === 4 || tx === 8 || tx === 9 || tx === 7 || tx === 3) nx = this.x;
                    const ty = getTileAt(this.x, ny);
                    if (ty === 1 || ty === 4 || ty === 8 || ty === 9 || ty === 7 || ty === 3) ny = this.y;
                    
                    // それでも壁に埋まっているなら移動しない（斜め等のエッジケース）
                    if (getTileAt(nx, ny) === 1) { nx = this.x; ny = this.y; }
                }
                this.x = nx; this.y = ny;
            }

            update(dt) {"""

content = re.sub(r"            update\(dt\) \{", move_method, content)

# update内の this.x += this.vx * dt; this.y += this.vy * dt; を this.move(dt); に置換
content = re.sub(r"this\.x \+= this\.vx \* dt; this\.y \+= this\.vy \* dt;", "this.move(dt);", content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Enemy collision fixed.")
