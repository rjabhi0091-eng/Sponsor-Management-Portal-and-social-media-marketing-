missing = open('missing.html', encoding='utf-8').read()
current = open('index.html', encoding='utf-8').read()
idx = current.find('<section id="registration-stats"')
if idx == -1:
    print("Could not find insertion point!")
else:
    new_content = current[:idx] + missing + '\n' + current[idx:]
    open('index.html', 'w', encoding='utf-8').write(new_content)
    print("Merge successful!")
