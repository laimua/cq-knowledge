import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\work\cq\README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace all GitHub links
text = text.replace('https://github.com/yourusername/cq.git', 'https://github.com/laimua/cq-knowledge.git')
text = text.replace('https://github.com/yourusername/cq/', 'https://github.com/laimua/cq-knowledge/')
text = text.replace('https://github.com/yourusername/cq"', 'https://github.com/laimua/cq-knowledge"')
text = text.replace('https://github.com/yourusername/cq', 'https://github.com/laimua/cq-knowledge')

with open(r'D:\work\cq\README.md', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

remaining = text.count('yourusername')
print(f'Done. Remaining yourusername: {remaining}')

# Verify Chinese is intact
lines = text.split('\n')
sample = lines[9][:30]
print(f'Line 10: {sample}')
