import re

with open('js/mapData.js', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r"('guild':\s*\{\s*width:\s*20,\s*height:\s*15,\s*tiles:\s*\[\s*)([\s\S]*?)(\s*\])"
match = re.search(pattern, c)

if match:
    tiles_str = match.group(2)
    lines = tiles_str.replace('\"', '').replace(' ', '').split(',')
    lines = [l for l in lines if l.strip()]
    
    if len(lines) > 2 and len(lines[1]) >= 11:
        row = list(lines[1])
        row[9] = 'h'
        row[10] = 'h'
        lines[1] = ''.join(row)
    
    new_tiles = ',\n                    '.join(['\"' + l + '\"' for l in lines])
    new_guild_data = match.group(1) + '\n                    ' + new_tiles + '\n                ' + match.group(3)
    
    c = c[:match.start()] + new_guild_data + c[match.end():]
    
    with open('js/mapData.js', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Added quest board to guild map!')
else:
    print('Failed to find guild map in mapData.js')
