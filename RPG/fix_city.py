import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def fix_city(m):
    return "'city': { type: 'city', portals: [\n                    { c: 40, r: 10, dest: 'guild', sc: 40, sr: 25 },\n                    { c: 40, r: 5, dest: 'dungeon_f1', sc: 40, sr: 74 }\n                ]"

# count=1 で最初の 'city' (または見つかったもの) のみ置換する。
# ただし、元々の tiles が消えないように portals までのみを置換する。
html = re.sub(r'\'city\': \{[\s\S]*?portals: \[[\s\S]*?\]', fix_city, html, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('City portals fixed')
