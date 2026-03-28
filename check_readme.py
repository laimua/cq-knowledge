import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\work\cq\README.md', 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8', errors='replace')
lines = text.split('\n')

# Check for replacement chars
repl_count = text.count('\ufffd')
print(f'Replacement chars: {repl_count}')

# Check line 10 (0-indexed 9) - should be **让 AI...
line = lines[9] if len(lines) > 9 else ''
print(f'Line 10 chars: {[(f"U+{ord(c):04X}", c) for c in line[:25]]}')
print(f'Line 10 text: {line[:50]}')

# Check if there are any bytes that are NOT valid UTF-8
try:
    raw.decode('utf-8')
    print('File is valid UTF-8')
except UnicodeDecodeError as e:
    print(f'Invalid UTF-8 at byte {e.start}-{e.end}: {raw[e.start:e.end].hex()}')
