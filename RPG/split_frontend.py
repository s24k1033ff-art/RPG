import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# sceneDataを探す
m = re.search(r'(const sceneData = \{[\s\S]*?\n        \};\n)', html)

if m:
    scene_data_str = m.group(1)
    
    # jsディレクトリを作成
    if not os.path.exists('js'):
        os.makedirs('js')
        
    # mapData.js に書き込む
    with open('js/mapData.js', 'w', encoding='utf-8') as f:
        f.write('// マップ、ポータル、敵、NPCの配置データ\n')
        f.write(scene_data_str)
        
    # index.html から sceneData の定義を削除
    html = html.replace(scene_data_str, '')
    
    # <script> タグの先頭に mapData.js を読み込むタグを追加
    # body の終わり付近の <script> タグを見つける
    html = html.replace('<script>', '<script src="js/mapData.js"></script>\n    <script>')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print('Separation successful! mapData.js created.')
else:
    print('Failed to find sceneData.')
