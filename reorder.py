import os

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_block(start_marker, end_marker_tag='section'):
    start_idx = -1
    for i, l in enumerate(lines):
        if start_marker in l:
            start_idx = i
            break
    if start_idx == -1: return None, -1, -1
    
    depth = 0
    for i in range(start_idx, len(lines)):
        if f'<{end_marker_tag}' in lines[i]:
            depth += lines[i].count(f'<{end_marker_tag}')
        if f'</{end_marker_tag}>' in lines[i]:
            depth -= lines[i].count(f'</{end_marker_tag}>')
            if depth <= 0:
                return lines[start_idx:i+1], start_idx, i
    return None, -1, -1

about_block, a_start, a_end = get_block('id="about"')
register_block, r_start, r_end = get_block('id="register"')

# create a new file by skipping the extracted blocks and inserting them at the right place
new_lines = []
i = 0
while i < len(lines):
    if i == a_start:
        i = a_end + 1
        continue
    if i == r_start:
        i = r_end + 1
        continue
        
    if '<section class="landing-features">' in lines[i]:
        # insert about here
        new_lines.extend(about_block)
        new_lines.append('\n')
        
    if 'id="registration-stats"' in lines[i]:
        # insert register here
        new_lines.extend(register_block)
        new_lines.append('\n')
        
    new_lines.append(lines[i])
    i += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Reordering successful.")
