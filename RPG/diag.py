with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('boss in file:', 'boss' in c)
print('mini_boss in file:', 'mini_boss' in c)
print('portal in file:', 'portal' in c)
print("'type === 'boss'' count:", c.count("type === 'boss'"))
# find lines with 'boss'
for i, line in enumerate(c.split('\n'), 1):
    if 'boss' in line.lower():
        print(f"L{i}: {line.strip()[:120]}")
