#!/usr/bin/env python3
"""Combina infra + artigos 1-11 + 12-23 + 24-41 + 42-58 em um unico script."""

import re

DIR = '/home/marcos/Desktop/AI/v4perettoco-main/projetos/seo/clientes/metal-indianapolis/seo-json'

# 1. Infrastructure from gerar_v3_originais.py
with open(f'{DIR}/gerar_v3_originais.py') as f:
    v3 = f.read()

# Extract just the helper functions + build + main (lines 78-369, from make_id to end)
lines = v3.split('\n')
infra = '\n'.join(l for l in lines if l.startswith(('def ', 'from ', 'import ', '', '#', 'DIR ', 'OUT_DIR ', 'HERO_IMG ', 'CONTATO_URL ', 'SITE_URL ', 'AUTHOR ', 'PUBLISHER ', 'ARTICLES')))
# Actually let me just take from line 1 to the first ARTICLES line
v3_lines = v3.split('\n')
# Find the main() function start and beyond
infra_start = 0
for i, l in enumerate(v3_lines):
    if l.strip().startswith('def make_id'):
        infra_start = i
        break

# We need: imports, constants, helper functions, but NOT ARTICLES list, NOT main content_for sections
# Take from line 0 up to line 76 (ARTICLES = [)
line0 = 0
for i, l in enumerate(v3_lines):
    if l.strip().startswith('ARTICLES'):
        line0 = i
        break

# Take lines 0 to ARTICLES line
infra_part = '\n'.join(v3_lines[:line0])

# Now take the build, main functions (from def build to end)
build_start = 0
for i, l in enumerate(v3_lines):
    if l.strip().startswith('def build'):
        build_start = i
        break

build_part = '\n'.join(v3_lines[build_start:])

# 2. Articles 1-11 from gerar_v4_unicos.py
with open(f'{DIR}/gerar_v4_unicos.py') as f:
    v4u = f.read()

# Find ARTICLES = [] or ARTICLES.append
art_start = 0
for i, l in enumerate(v4u.split('\n')):
    if 'ARTICLES.append' in l:
        art_start = i
        break

# Get just the append blocks (skip header)
articles_1_11 = '\n'.join(v4u.split('\n')[art_start-2:])  # include ARTICLES = []

# 3. Articles 12-23
with open('/home/marcos/Desktop/AI/v4perettoco-main/articles_output.py') as f:
    articles_12_23 = f.read()

# 4. Articles 24-41
with open('/tmp/artigos_metal_indianapolis.py') as f:
    a24_raw = f.read()
a24_lines = a24_raw.split('\n')
art24_start = next(i for i,l in enumerate(a24_lines) if l.startswith('ARTICLES.append'))
art24_end = next(i for i in range(art24_start, len(a24_lines)) if a24_lines[i].strip().startswith(('for ', 'print(')))
articles_24_41 = '\n'.join(a24_lines[art24_start:art24_end])

# 5. Articles 42-58
with open('/home/marcos/.local/share/opencode/tool-output/tool_f1487197d001lACFFCdIpUhnUN') as f:
    a42_raw = f.read()
blocks = re.findall(r'```python\n(.*?)```', a42_raw, re.DOTALL) or re.findall(r'```\n(.*?)```', a42_raw, re.DOTALL)
articles_42_58 = '\n'.join(blocks)

# 6. Assemble
output_parts = [
    infra_part,
    '\nARTICLES = []\n',
    articles_1_11.lstrip(),
    '\n',
    articles_12_23.lstrip(),
    '\n',
    articles_24_41.lstrip(),
    '\n',
    articles_42_58.lstrip(),
    '\n',
    build_part,
]

full = ''.join(output_parts)

# 7. Fix the bracket pattern in articles 42-58
# Pattern: ")]), [\n    ("  -> should be "]), [\n    ("
full = full.replace(')]), [\n    (', ']), [\n    (')

# 8. Ensure main() is called at the end
if 'if __name__ == "__main__":' not in full.split('\n')[-5]:
    full += '\nif __name__ == "__main__":\n    main()\n'

# Count articles
count = full.count('ARTICLES.append')
print(f'Total ARTICLES.append blocks: {count}')
print(f'Total lines: {len(full.splitlines())}')

# Try compile
# Write first, then check
with open(f'{DIR}/gerador_completo.py', 'w') as f:
    f.write(full)
print(f'Written to gerador_completo.py')

try:
    compile(full, 'gerador_completo.py', 'exec')
    print('Compile: OK')
except SyntaxError as e:
    print(f'Compile ERROR at line {e.lineno}: {e.msg}')
    lines = full.split('\n')
    start = max(0, e.lineno-5)
    end = min(len(lines), e.lineno+2)
    for i in range(start, end):
        marker = '>>>' if i+1 == e.lineno else '   '
        print(f'  {marker} {i+1}: {lines[i]}')
