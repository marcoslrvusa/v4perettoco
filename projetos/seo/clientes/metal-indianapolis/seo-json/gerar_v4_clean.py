#!/usr/bin/env python3
"""Fix the )]), [ pattern in gerar_v4_clean.py"""
import re

with open('gerar_v4_clean.py') as f:
    content = f.read()

# Pattern: ")]), [\n    ("
# Should be: "]), [\n    ("
# (removing the extra closing paren before the bracket)

# Use regex to find the pattern
pattern = r'\)\]\),\s*\n\s*\('
replacement = r']),\n    ('

fixed = re.sub(pattern, replacement, content)

# Check remaining
remaining = fixed.count(')]), [')
print(f'Remaining incorrect patterns: {remaining}')

with open('gerar_v4_clean.py', 'w') as f:
    f.write(fixed)

# Try compile
try:
    compile(fixed, 'gerar_v4_clean.py', 'exec')
    print('Compile: OK')
except SyntaxError as e:
    print(f'Compile ERROR at line {e.lineno}: {e.msg}')
    lines = fixed.split('\n')
    for i in range(max(0, e.lineno-2), min(len(lines), e.lineno+2)):
        print(f'  {i+1}: {lines[i]}')
