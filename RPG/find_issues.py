import re
with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Number of fullscreen logics:', c.count("if (key === 'f') {"))
print('Number of level scale codes:', c.count('const levelBonus = (floorLevel - 1) * 5;'))

lines = c.split('\n')
for i, line in enumerate(lines):
    if "key === 'escape'" in line:
        print(f'Line {i+1}: {line}')
