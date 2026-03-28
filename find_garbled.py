"""Fix ALL garbled characters in README.md by examining raw bytes carefully."""
import sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')

result = subprocess.run(
    ['git', 'show', 'HEAD:README.md'],
    capture_output=True, cwd=r'D:\work\cq'
)
raw = result.stdout
text = raw.decode('utf-8', errors='replace')

# Find all replacement characters and their context
lines = text.split('\n')
issues = []
for i, line in enumerate(lines):
    pos = 0
    while True:
        idx = line.find('\ufffd', pos)
        if idx == -1:
            break
        # Get surrounding context (5 chars before and after)
        start = max(0, idx - 5)
        end = min(len(line), idx + 10)
        context = line[start:end]
        issues.append((i+1, idx, context))
        pos = idx + 1

print(f'Total garbled positions: {len(issues)}')
for line_no, col, ctx in issues[:30]:
    print(f'  Line {line_no}, col {col}: ...{repr(ctx)}...')

if len(issues) > 30:
    print(f'  ... and {len(issues)-30} more')
