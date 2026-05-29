import re
with open('perfect_safe_patch.py', 'r', encoding='utf-8') as f:
    script = f.read()

script = script.replace('quest_board, html)', 'interact_logic, html)')

with open('perfect_safe_patch.py', 'w', encoding='utf-8') as f:
    f.write(script)
