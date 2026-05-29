with open('preview_demo.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
scenes = re.findall(r"'(\w+)'\s*:\s*\{\s*width:\s*\d+,\s*height:\s*\d+,\s*tiles:\s*\[", content)
print('Found scenes:', scenes)
