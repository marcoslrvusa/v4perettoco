#!/usr/bin/env python3
"""Combina os 58 artigos de 4 fontes e executa o gerador final."""

import sys
import os

# 1. Read the base script (infrastructure + articles 1-11)
with open('gerar_v4_unicos.py') as f:
    base = f.read()

# 2. Remove the placeholder text after the last article (articles 1-11 go to end of file)
# The base file has articles 1-11 then "Continue writing builder" at the end
base = base.replace('\n# Continue writing builder\n', '')

# 3. Read articles 12-23
with open('/home/marcos/Desktop/AI/v4perettoco-main/articles_output.py') as f:
    data_12_23 = f.read()

# 4. Read articles 24-41
with open('/tmp/artigos_metal_indianapolis.py') as f:
    data_24_41 = f.read()
lines = data_24_41.strip().split('\n')
# Find first ARTICLES.append
start = 0
for i, l in enumerate(lines):
    if l.startswith('ARTICLES.append'):
        start = i
        break
# Find end (print or for loop)
end = len(lines)
for i in range(start, len(lines)):
    stripped = lines[i].strip()
    if stripped.startswith('for ') or stripped.startswith('print('):
        end = i
        break
data_24_41_clean = '\n'.join(lines[start:end])

# 5. Read articles 42-58 - extract from markdown code blocks
with open('/home/marcos/.local/share/opencode/tool-output/tool_f1487197d001lACFFCdIpUhnUN') as f:
    data_42_58 = f.read()

# Extract code blocks
import re
blocks = re.findall(r'```python\n(.*?)```', data_42_58, re.DOTALL)
if not blocks:
    # Try without python language tag
    blocks = re.findall(r'```\n(.*?)```', data_42_58, re.DOTALL)
data_42_58_clean = '\n'.join(blocks) if blocks else ''

# Count articles
count_12_23 = data_12_23.count('ARTICLES.append')
count_24_41 = data_24_41_clean.count('ARTICLES.append')
count_42_58 = data_42_58_clean.count('ARTICLES.append')
print(f'Artigos 01-11: ja no base (11)')
print(f'Artigos 12-23: {count_12_23}')
print(f'Artigos 24-41: {count_24_41}')
print(f'Artigos 42-58: {count_42_58}')

# Concatenate everything
full = base + '\n\n' + data_12_23 + '\n\n' + data_24_41_clean + '\n\n' + data_42_58_clean

# Count total
total = full.count('ARTICLES.append')
print(f'Total: {total}')

# Now add the main function call at the end
full += '\n\nif __name__ == "__main__":\n    main()\n'

# Write the final script
out_path = 'gerar_v4_final.py'
with open(out_path, 'w') as f:
    f.write(full)

print(f'Script final escrito em {out_path}')
print(f'Total de linhas: {len(full.splitlines())}')
