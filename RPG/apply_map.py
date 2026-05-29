import re

with open('map_out.txt', 'r', encoding='utf-8') as f:
    new_tiles = f.read()

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 正規表現で city の tiles 配列を置換
pattern = r"('city':\s*\{\s*width:\s*80,\s*height:\s*60,[^{}]*?)\s*tiles:\s*\[[\s\S]*?\],"
replacement = r'\1' + '\n' + new_tiles

new_content = re.sub(pattern, replacement, content)

# portals と npcs の座標も置換
pattern_portals = r"(portals:\s*\[\s*)\{ c: 10, r: 24, dest: 'guild', sc: 10, sr: 13 \},\s*\{ c: 20, r: 24, dest: 'blacksmith', sc: 10, sr: 13 \},\s*\{ c: 40, r: 55, dest: 'dungeon_f1', sc: 40, sr: 4 \}\s*\]"
replacement_portals = r"\1{ c: 25, r: 20, dest: 'guild', sc: 10, sr: 13 },\n                    { c: 30, r: 35, dest: 'blacksmith', sc: 10, sr: 13 },\n                    { c: 75, r: 30, dest: 'dungeon_f1', sc: 40, sr: 4 }\n                ]"
new_content = re.sub(pattern_portals, replacement_portals, new_content)

new_content = new_content.replace("{ c: 40, r: 35, id: 'guide', name: \"ベテラン冒険者\" }", "{ c: 40, r: 28, id: 'guide', name: \"ベテラン冒険者\" }")

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done!')
