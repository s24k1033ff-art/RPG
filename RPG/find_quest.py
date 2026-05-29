import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()
for m in re.finditer(r'(questBoard|activeQuest|questProgress|loadScene|function loadScene|getFloorLevel|floorLevel|upgradeWeapon)', c):
    line_no = c[:m.start()].count('\n') + 1
    line = c.split('\n')[line_no-1].strip()[:150]
    print(f"L{line_no}: {line}")
