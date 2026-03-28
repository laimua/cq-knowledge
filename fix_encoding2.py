"""Fix garbled Chinese in README.md by removing UTF-8 replacement characters
and restoring the correct text."""

with open(r'D:\work\cq\README.md', 'rb') as f:
    raw = f.read()

# The pattern: \xef\xbf\xbd followed by a byte that was part of the original char
# We need to manually fix known garbled sequences

text = raw.decode('utf-8', errors='replace')

# Known garbled text and their corrections
fixes = {
    '让': '让',
}

# Find all replacement chars and their context
import re
# Pattern: \ufffd followed by one char then correct text
# The original had multi-byte UTF-8 chars that got corrupted

# Let's find all lines with replacement chars and fix them
lines = text.split('\n')
fixed_lines = []

known_fixes = {
    '\ufffd?AI': '让 AI',
    '专\ufffd': '专为',
    '但服务\ufffd': '但服务于',
    '解决的问\ufffd': '解决的问题',
    '知\ufffd库': '知识库',
    '条\ufffd': '条件',
    '创\ufffd': '创建',
    '编\ufffd': '编码',
    '详\ufffd': '详细',
    '验\ufffd': '验证',
    '认\ufffd': '认证',
    '设\ufffd': '设置',
    '配\ufffd': '配置',
    '选\ufffd': '选择',
    '请\ufffd': '请求',
    '检\ufffd': '检索',
    '注\ufffd': '注册',
    '缓\ufffd': '缓存',
    '快\ufffd': '快速',
    '数\ufffd': '数量',
    '优\ufffd': '优化',
    '改\ufffd': '改进',
    '完\ufffd': '完善',
    '记\ufffd': '记录',
    '实\ufffd': '实现',
    '参\ufffd': '参考',
    '访\ufffd': '访问',
    '权\ufffd': '权限',
    '功\ufffd': '功能',
    '连\ufffd': '连接',
    '操\ufffd': '操作',
    '控\ufffd': '控制',
    '测\ufffd': '测试',
    '调\ufffd': '调试',
    '解\ufffd': '解决',
    '处\ufffd': '处理',
    '转\ufffd': '转换',
    '删\ufffd': '删除',
    '查\ufffd': '查询',
    '激\ufffd': '激活',
    '查\ufffd': '查询',
    '据\ufffd': '数据',
    '文\ufffd': '文档',
    '输\ufffd': '输出',
    '执\ufffd': '执行',
    '返\ufffd': '返回',
    '响\ufffd': '响应',
    '据\ufffd': '数据',
    '命\ufffd': '命令',
    '触\ufffd': '触发',
    '引\ufffd': '引用',
    '展\ufffd': '展示',
    '认\ufffd': '认证',
    '指\ufffd': '指定',
    '高\ufffd': '高级',
    '数\ufffd': '数量',
    '协\ufffd': '协议',
    '其\ufffd': '其他',
    '协\ufffd': '协作',
    '支\ufffd': '支持',
    '通\ufffd': '通过',
    '为\ufffd': '为',
    '以\ufffd': '以',
    '已\ufffd': '已',
    '并\ufffd': '并',
    '可\ufffd': '可',
    '与\ufffd': '与',
    '对\ufffd': '对',
    '下\ufffd': '下',
    '从\ufffd': '从',
    '在\ufffd': '在',
    '个\ufffd': '个',
    '之\ufffd': '之',
    '是\ufffd': '是',
    '和\ufffd': '和',
    '或\ufffd': '或',
    '等\ufffd': '等',
    '中\ufffd': '中',
    '会\ufffd': '会',
    '都\ufffd': '都',
    '能\ufffd': '能',
    '将\ufffd': '将',
    '被\ufffd': '被',
    '要\ufffd': '要',
    '有\ufffd': '有',
    '也\ufffd': '也',
    '就\ufffd': '就',
    '这\ufffd': '这',
    '不\ufffd': '不',
    '而\ufffd': '而',
    '的\ufffd': '的',
    '了\ufffd': '了',
    '到\ufffd': '到',
    '用\ufffd': '用',
    '时\ufffd': '时',
    '需\ufffd': '需',
    '包\ufffd': '包含',
    '的\ufffd': '的',
}

# Better approach: just find \ufffd and try to figure out what's missing
# Actually, let's look at the raw bytes more carefully
# The pattern is: \xef\xbf\xbd (3 bytes for U+FFFD) followed by one ASCII char
# The original was likely a 4-byte UTF-8 char where first 3 bytes became replacement

# Actually looking at the hex: 2a2a efbfbd 3f 4149...
# \xef\xbf\xbd = U+FFFD, then 0x3f = '?'
# The original "让" in UTF-8 is e8 ae a9 (3 bytes)
# But we see ef bf bd 3f = replacement char + '?'
# So it seems like the first byte was corrupted and the rest survived

# Let me just do targeted replacements based on context
for i, line in enumerate(lines):
    if '\ufffd' in line:
        # Print for debugging
        print(f"Line {i+1}: {line[:100]}")

# Actually let's take a different approach - look at what the Chinese SHOULD be
# and just write the correct README from scratch based on the garbled one
