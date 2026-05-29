import re

with open('map_out.txt', 'r', encoding='utf-8') as f:
    f1_data = f.read()

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"'dungeon_f1':\s*\{\s*width:\s*80,\s*height:\s*80,[\s\S]*?getTheme:\s*\(\)\s*=>\s*themes\.dungeon\s*\}"

replacement = "'dungeon_f1': {\n                width: 80, height: 80,\n                " + f1_data + "                getTheme: () => themes.dungeon\n            }"

new_content = re.sub(pattern, replacement, content)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done!')
