import re

with open('refactor_enemy_ai.py', 'r', encoding='utf-8', errors='replace') as f:
    script = f.read()

# refactor_enemy_ai.py から enemy_class の定義文字列を抽出
match = re.search(r'enemy_class = \"\"\"(.*?)\"\"\"', script, re.DOTALL)
if match:
    enemy_code = match.group(1)
    
    with open('preview_demo.html', 'r', encoding='utf-8') as html_file:
        html = html_file.read()
        
    # 壊れた class Enemy を置換
    # class Enemy { から class EnemyProjectile { の前まで
    broken_enemy_pattern = r'class Enemy \{[\s\S]*?(?=class EnemyProjectile \{)'
    
    level_scale = '''
                let floorLevel = 1;
                if (currentSceneId && currentSceneId.startsWith('dungeon_f')) {
                    floorLevel = parseInt(currentSceneId.split('_f')[1]);
                }
                const levelBonus = (floorLevel - 1) * 5;
                this.level = 1 + levelBonus;
                this.maxHp = Math.floor(this.maxHp * (1 + levelBonus * 0.1));
                this.hp = this.maxHp;
                if (this.atk) this.atk = Math.floor(this.atk * (1 + levelBonus * 0.1));
                this.xp += levelBonus * 5;
                this.gold += levelBonus * 2;
    '''
    # 元の enemy_code の this.hp = this.maxHp; の前に追加
    fixed_enemy_code = enemy_code.replace('this.hp = this.maxHp;', level_scale)
    
    new_html = re.sub(broken_enemy_pattern, fixed_enemy_code + '\n        ', html)
    
    with open('preview_demo.html', 'w', encoding='utf-8') as html_file:
        html_file.write(new_html)
    print('Restored and patched Enemy class!')
else:
    print('Failed to extract enemy_class')
