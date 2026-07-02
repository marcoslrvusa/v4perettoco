#!/usr/bin/env python3
import re

with open('gerar_v4_clean.py') as f:
    content = f.read()

# Check for the problematic pattern ")]), ["
matches = [(m.start(), m.group()) for m in re.finditer(r'\)\]\),\s*\[', content)]
print(f"Pattern ')]), [' found {len(matches)} times")
for pos, m in matches[:5]:
    ctx = content[max(0,pos-40):pos+20]
    print(f"  pos {pos}: ...{ctx}...")

# Try compile
try:
    compile(content, 'gerar_v4_clean.py', 'exec')
    print("Compile: OK")
except SyntaxError as e:
    print(f"Compile ERROR: {e}")
    # Show context around error
    lines = content.split('\n')
    lineno = e.lineno
    for i in range(max(0,lineno-3), min(len(lines), lineno+2)):
        marker = ">>>" if i+1 == lineno else "   "
        print(f"  {marker} {i+1}: {lines[i]}")
