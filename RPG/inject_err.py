import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

handler = """<script>
window.onerror = function(msg, url, line) {
    alert('Error: ' + msg + '\\nLine: ' + line);
    return false;
};
</script>
<script src="js/constants.js"></script>"""

c = c.replace('<script src="js/constants.js"></script>', handler)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Injected!")
