with open('preview_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

print('Number of requestFullscreen:', c.count('requestFullscreen'))
print('Number of escape keys:', c.count("key === 'escape'"))

lines = c.split('\n')
for i, line in enumerate(lines):
    if "key === 'escape'" in line:
        print(f'L{i+1}: {line.strip()}')

# 簡易的な JS 構文エラーチェック (中括弧の対応)
try:
    js = c.split('<script>')[1].split('</script>')[0]
    brace_count = 0
    in_string = False
    string_char = ''
    in_comment = False
    i = 0
    while i < len(js):
        char = js[i]
        if in_comment:
            if char == '\\n':
                in_comment = False
            i += 1
            continue
            
        if in_string:
            if char == '\\\\' :
                i += 2
                continue
            if char == string_char:
                in_string = False
            i += 1
            continue
            
        if char in ["'", '"', '`']:
            in_string = True
            string_char = char
        elif char == '/' and i+1 < len(js) and js[i+1] == '/':
            in_comment = True
            i += 1
        elif char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count < 0:
                print(f'Negative brace count around index {i}')
                print('Context:', js[i-50:i+50])
                break
        i += 1
    print('Final brace count:', brace_count)
except Exception as e:
    print('Parse error:', e)
