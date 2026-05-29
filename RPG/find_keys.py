with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()
import re
# find key event handling
for m in re.finditer(r'(addEventListener|onkey|keys\[)', c):
    line_no = c[:m.start()].count('\n') + 1
    line = c.split('\n')[line_no-1].strip()[:150]
    print(f"L{line_no}: {line}")
