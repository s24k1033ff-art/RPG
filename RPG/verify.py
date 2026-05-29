with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()
import re
scenes = re.findall(r"'(dungeon_f\d+)'\s*:", c)
print('Dungeon scenes found:', scenes)
themes = re.findall(r"(dungeon_f\d+):\s*\{", c)
print('Themes found:', themes)
# Check portal chain
portals = re.findall(r"nextDest = '(dungeon_f\d+|city)'", c)
print('Portal chain targets:', portals)
print('File size:', len(c), 'bytes')
