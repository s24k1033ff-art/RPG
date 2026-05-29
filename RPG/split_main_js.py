import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# <script> の中身を抽出 (mapData.js の script タグの直後にあるメインの script タグ)
# re.DOTALL (re.S) を使って複数行をマッチさせる
m = re.search(r'<script>\n(.*?)    </script>', html, re.DOTALL)

if m:
    main_js_str = m.group(1)
    
    # main.js に書き込む
    with open('js/main.js', 'w', encoding='utf-8') as f:
        f.write(main_js_str)
        
    # index.html のメインの <script> の中身を消し、 src="js/main.js" に置き換える
    html = html.replace('<script>\n' + main_js_str + '    </script>', '<script src="js/main.js"></script>')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print('Separation successful! main.js created.')
else:
    print('Failed to find main script block.')
