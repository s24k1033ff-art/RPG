import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# プレイヤーのupdate / move を探す
lines = c.split('\n')
for i, line in enumerate(lines):
    if 'function update(dt)' in line or 'player.x += dx' in line or 'function render' in line:
        print(f"L{i+1}: {line.strip()[:100]}")
