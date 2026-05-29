import re

with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 誤って挿入された2回目の level scale を元に戻す
bad_code = """
                        this.x = this.spawnX; this.y = this.spawnY;
                        
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
 this.state = 'idle';
                    }
                    return;
                }"""

good_code = """
                        this.x = this.spawnX; this.y = this.spawnY;
                        this.hp = this.maxHp; this.state = 'idle';
                    }
                    return;
                }"""

# 厳密にマッチするか確認して置換
c = c.replace(bad_code, good_code)

# もし exact match が失敗した場合のために、正規表現で置換
if bad_code not in c:
    pattern = r"this\.x = this\.spawnX; this\.y = this\.spawnY;[\s\S]*?this\.state = 'idle';\s*\}\s*return;\s*\}"
    c = re.sub(pattern, good_code.strip(), c)

with open('preview_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed enemy respawn bug!")
