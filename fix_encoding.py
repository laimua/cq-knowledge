import sys

with open(r'D:\work\cq\README.md', 'rb') as f:
    raw = f.read()

for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin1', 'cp1252']:
    try:
        text = raw.decode(enc)
        # Check for known Chinese characters
        test_chars = ['让', '编码', '代理', '学习']
        found = [c for c in test_chars if c in text]
        if found:
            print(f'{enc}: found {found[:3]}')
    except:
        pass

# Show raw bytes around position 200-300
print('---')
print(raw[180:220].hex())
