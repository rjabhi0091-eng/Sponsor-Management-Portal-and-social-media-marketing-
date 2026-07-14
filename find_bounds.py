import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_tag_end(start_line, tag_name='section'):
    depth = 0
    for i in range(start_line, len(lines)):
        if f'<{tag_name}' in lines[i]:
            depth += lines[i].count(f'<{tag_name}')
        if f'</{tag_name}>' in lines[i]:
            depth -= lines[i].count(f'</{tag_name}>')
            if depth <= 0:
                return i
    return -1

about_start = next(i for i, l in enumerate(lines) if 'id="about"' in l and '<section' in l)
about_end = find_tag_end(about_start)

register_start = next(i for i, l in enumerate(lines) if 'id="register"' in l and '<section' in l)
register_end = find_tag_end(register_start)

print(f"About: {about_start+1} to {about_end+1}")
print(f"Register: {register_start+1} to {register_end+1}")
