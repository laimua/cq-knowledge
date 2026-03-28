"""Check raw bytes around known garbled areas in the git HEAD version."""
import sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')

result = subprocess.run(
    ['git', 'show', 'HEAD:README.md'],
    capture_output=True, cwd=r'D:\work\cq'
)
raw = result.stdout
text = raw.decode('utf-8')

# Line 10 should be: **让 AI 编码代理相互学习，避免重复犯错，减少 token 浪费**
lines = text.split('\n')
print(f'Line 10: {repr(lines[9])}')

# Check byte-level: find "**" near "AI"
# "**让" in UTF-8: 2a2a E8AEA9
target = b'** AI'  # This is what it might look like if 让 is missing
idx = raw.find(target)
print(f'Found "** AI" at byte {idx}: {raw[idx:idx+30].hex()}')

# Also search for "**\n" patterns near AI  
for i in range(len(raw)):
    if raw[i:i+4] == b'**\n' and i > 400 and i < 600:
        print(f'Found **\\n at byte {i}: {raw[i:i+40].hex()}')
        print(f'  text: {repr(raw[i:i+40].decode("utf-8", errors="replace"))}')

# Find all lines and check for incomplete Chinese sequences
# A 3-byte UTF-8 char starts with E0-EF, followed by 80-BF, 80-BF
# Check for truncated sequences
print('\n--- Checking for truncated UTF-8 sequences ---')
i = 0
count = 0
while i < len(raw) - 2:
    b = raw[i]
    if 0xE0 <= b <= 0xEF:  # Start of 3-byte sequence
        if i + 2 >= len(raw):
            print(f'  Truncated 3-byte seq at byte {i}: {raw[i:].hex()}')
            count += 1
            break
        b1, b2 = raw[i+1], raw[i+2]
        if not (0x80 <= b1 <= 0xBF and 0x80 <= b2 <= 0xBF):
            print(f'  Invalid 3-byte seq at byte {i}: {raw[i:i+3].hex()} -> {repr(raw[i:i+6].decode("utf-8", errors="replace"))}')
            count += 1
            if count > 20: break
    i += 1
print(f'Found {count} issues')
