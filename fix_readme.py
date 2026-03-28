"""Fix all garbled UTF-8 replacement characters in README.md"""
import re

with open(r'D:\work\cq\README.md', 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8', errors='replace')

# Map: (replacement_char + following_context) -> correct_text
# The \ufffd represents a missing Chinese character
fixes = [
    # Line 10
    ('\ufffd?AI ', '让 AI '),
    # Line 22
    ('专\ufffdAI', '专为AI'),
    ('平台\ufffd\n', '平台。\n'),
    # Line 23
    ('服务\ufffdAI', '服务于AI'),
    ('Agents\ufffd?*', 'Agents。*'),
    # Line 25
    ('问\ufffd\n', '问题\n'),
    # Line 28
    ('大\ufffdtoken', '大量token'),
    # Line 30
    ('共\ufffd*|', '共享*|'),
    # Line 32
    ('\ufffd核心', '🎯核心'),
    # Line 36
    ('中英\ufffd|', '中英文|'),
    # Line 37
    ('管\ufffd*|', '管理*|'),
    # Line 38
    ('置信\ufffd*|', '置信度*|'),
    ('评\ufffd|', '评分|'),
    # Line 40
    ('集成\ufffdClaude', '集成到Claude'),
    # Line 41
    ('安\ufffd|', '安全|'),
    # Line 42
    ('迁\ufffd|', '迁移|'),
    # Line 44
    ('开\ufffd\n', '开始\n'),
    # Line 51
    ('使\ufffduvx', '使用uvx'),
    # Line 58
    ('db\ufffdcq', 'db，cq'),
    # Line 61
    ('知\ufffd\n', '知识\n'),
    # Line 66
    ('使\ufffduseCallback', '使用useCallback'),
    # Line 79
    ('config.json\ufffdcq', 'config.json：\n\n# Claude Code 中使用\n>cq'),
    # Line 92
    ('关\ufffdReact', '关于React'),
    ('知\ufffd\n', '知识\n'),
    # Line 93
    ('参\ufffd\n', '参考\n'),
    # Line 98
    ('关键\ufffd --limit', '关键词 --limit'),
    # Line 105
    ('置信\ufffd|', '置信度|'),
    # Line 115
    ('标\ufffd \\', '标题 \\'),
    # Line 122
    ('默\ufffd|', '默认值|'),
    # Line 127
    ('标\ufffd|', '标签|'),
    ('| \ufffd|', '| 无|'),
    # Line 128
    ('置信\ufffd(0-1)', '置信度(0-1)'),
    # Line 133
    ('关键\ufffd --limit', '关键词 --limit'),
    # Line 136
    ('默\ufffd|', '默认值|'),
    # Line 138
    ('参数\ufffd|', '参数）|'),
    # Line 140
    ('过\ufffd|', '过滤|'),
    ('| \ufffd|', '| 无|'),
    # Line 145
    ('帮\ufffd\n', '帮助\n'),
    # Line 148
    ('默\ufffd|', '默认值|'),
    # Line 152
    ('| \ufffd|', '| 无|'),
    # Line 154
    ('帮\ufffd\ufffd1-3', '帮助"，1-3'),
    # Line 162
    ('存在\ufffdcq', '存在的）\n\ncq'),
    # Line 189
    ('参\ufffd|', '参数|'),
    # Line 199
    ('\ufffdClaude', '在Claude'),
    # Line 201
    ('知\ufffd\n', '知识\n'),
    # Line 202
    ('标\ufffd\ufffd解决', '标题为"解决'),
    ('冲\ufffd\ufffd解决', '冲突"，解决方案是"'),
    ('标\ufffd\ufffd', '标题为"'),
    ('冲\ufffd\ufffd', '冲突"，'),
    # Line 204
    ('好\ufffd\n', '好评\n'),
    # Line 222
    ('客\ufffd\n', '客户端\n'),
    # Line 223
    ('支\ufffdMCP', '支持MCP'),
    ('集成\ufffd\n', '集成。\n'),
    # Line 234
    ('文档\ufffd\n', '文档。\n'),
    # Line 239
    ('检\ufffd|', '检查|'),
    # Line 247
    ('示\ufffd\n', '示例\n'),
    # Line 253
    ('实\ufffd,', '实践",'),
    # Line 254
    ('信\ufffd,', '信息",'),
    # Line 255
    ('属\ufffd,', '属性",'),
    # Line 263
    ('饰\ufffd,', '装饰器",'),
    # Line 279
    ('设\ufffdAccess', '设置Access'),
    # Line 288
    ('说\ufffd\n', '说明\n'),
    # Line 289
    ('范\ufffd0.1', '范围0.1'),
    # Line 290
    ('置信\ufffd|', '置信度|'),
    # Line 292
    ('反\ufffd|', '反馈|'),
    ('默\ufffd|', '默认值|'),
    # Line 295
    ('计\ufffd|', '计算|'),
    # Line 297
    ('公式\ufffd\n', '公式：\n'),
    # Line 302
    ('置信\ufffd*\ufffd', '置信度：'),
    # Line 310
    ('知\ufffdcq', '知识的）\n\ncq'),
    # Line 313
    ('\ufffd系统', '🏗 系统'),
    # Line 316
    ('\ufffd\ufffd                        Cq', '┐                        Cq'),
    # Line 318
    ('知\ufffd\ufffd', '知识 →'),
    ('索引\ufffd\n', '索引）\n'),
    # Line 319
    ('排序\ufffd\ufffd', '排序 →'),
    # Line 320
    ('置信\ufffd```', '置信度\n```'),
    # Line 322
    ('\ufffd常见', '❓常见'),
    # Line 327
    ('db\ufffd\ufffdSQLite', 'db（SQLite'),
    ('路\ufffd\ufffd', '路径：'),
    ('设\ufffd环境', '设置环境'),
    # Line 349
    ('关键\ufffd2.', '关键词2.'),
    # Line 355
    ('看不\ufffdMCP', '看不到MCP'),
    # Line 383
    ('帮\ufffd\ufffd1', '帮助"，1'),
    ('评\ufffd\ufffd1', '评分"，1'),
    ('评\ufffd-', '评分-'),
    # Line 385
    ('说\ufffd\ufffd<', '说明。</details>'),
    # Line 390
    ('是\ufffd', '是的'),
    # Line 397
    ('\ufffd开\ufffd', '🛠 开'),
    # Line 403
    ('依\ufffdpip', '依赖：\n\npip'),
    # Line 408
    ('检\ufffdcq', '检查：\n\nruff check cq/'),
    # Line 411
    ('测\ufffdpytest', '测试：\n\npytest'),
    # Line 422
    ('状\ufffd\n', '状态\n'),
    # Line 423
    ('\ufffd核心', '✅核心'),
    # Line 424
    ('\ufffdCLI', '✅CLI'),
    # Line 425
    ('\ufffd数据', '✅数据'),
    # Line 426
    ('\ufffdMCP', '✅MCP'),
    # Line 427
    ('\ufffd文档', '✅文档'),
    # Line 433
    ('许\ufffd\n', '许可证\n'),
    # Line 454
    ('\ufffdCore', '🎯Core'),
    # Line 753
    ('\ufffdSystem', '🏗System'),
    # Line 756
    ('\ufffd\ufffd                        Cq', '┐                        Cq'),
    # Line 758
    ('索引\ufffd\n', 'index）\n'),
    # Line 763
    ('\ufffdFAQ', '❓FAQ'),
    # Line 845
    ('\ufffdDevel', '🛠 Devel'),
    # Line 876
    ('\ufffdCore', '✅Core'),
    # Line 877
    ('\ufffdCLI', '✅CLI'),
    # Line 878
    ('\ufffdData', '✅Data'),
    # Line 879
    ('\ufffdMCP', '✅MCP'),
    # Line 880
    ('\ufffdDocu', '✅Docu'),
]

for old, new in fixes:
    text = text.replace(old, new)

# Check remaining \ufffd
remaining = [(i, line) for i, line in enumerate(text.split('\n')) if '\ufffd' in line]
if remaining:
    print(f"WARNING: {len(remaining)} lines still have garbled chars:")
    for i, line in remaining:
        print(f"  Line {i+1}: {line[:80]}")
else:
    print("All garbled characters fixed!")

# Write back as UTF-8 no BOM
utf8 = new
with open(r'D:\work\cq\README.md', 'w', encoding='utf-8', newline='') as f:
    f.write(text)
