# Cq CLI 命令参考

完整的 Cq 命令行工具参考文档。

## 命令概览

| 命令 | 简写 | 说明 |
|------|------|------|
| `version` | - | 显示版本信息 |
| `init` | - | 初始化知识库 |
| `add` | - | 添加知识单元 |
| `search` | - | 搜索知识 |
| `list` | - | 列出知识 |
| `show` | - | 查看知识详情 |
| `feedback` | - | 添加反馈 |
| `delete` | - | 删除知识 |
| `export` | - | 导出知识库 |
| `import-cmd` | - | 导入知识库 |
| `recalculate` | - | 重算置信度 |
| `serve` | - | 启动 API 服务 |

## 命令详解

### version

显示 Cq 版本信息。

```bash
cq-knowledge version
```

**输出示例**：
```
Cq version 0.1.0
```

---

### init

初始化知识库数据库。

```bash
cq-knowledge init
```

**说明**：
- 在 `~/.cq/` 目录创建 `knowledge.db` SQLite 数据库
- 自动创建必要的表和 FTS5 全文搜索索引
- 如果数据库已存在，不会覆盖

**输出示例**：
```
Initializing knowledge base...
✓ Knowledge base initialized at /home/user/.cq/knowledge.db
```

---

### add

添加新的知识单元到知识库。

```bash
cq-knowledge add --title <标题> --problem <问题> --solution <解决方案> [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--title` | `-t` | string | ✅ | - | 知识标题 |
| `--problem` | `-p` | string | ✅ | - | 问题描述 |
| `--solution` | `-s` | string | ✅ | - | 解决方案 |
| `--tags` | - | string | ❌ | 空 | 逗号分隔的标签 |
| `--confidence` | `-c` | float | ❌ | 0.5 | 置信度 (0-1) |

**示例**：

```bash
# 基础用法
cq-knowledge add \
  --title "React useEffect 无限循环" \
  --problem "useEffect 依赖数组导致无限循环" \
  --solution "确保依赖数组包含所有外部变量" \
  --tags "react,hooks"

# 带置信度
cq-knowledge add \
  -t "Python 装饰器最佳实践" \
  -p "装饰器改变了原函数的元信息" \
  -s "使用 functools.wraps 保留元信息" \
  --tags "python,decorator" \
  --confidence 0.95
```

**输出示例**：
```
✓ Knowledge unit added: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: React useEffect 无限循环
  Tags: react, hooks
```

---

### search

使用 FTS5 全文搜索查找知识。

```bash
cq-knowledge search <查询关键词> [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `query` | - | string | ✅ | - | 搜索关键词（位置参数） |
| `--limit` | `-l` | int | ❌ | 10 | 返回结果数量 |
| `--tag` | - | string | ❌ | - | 按标签过滤 |

**示例**：

```bash
# 简单搜索
cq-knowledge search "useEffect"

# 限制结果数量
cq-knowledge search "asyncio" --limit 5

# 按标签过滤
cq-knowledge search "循环" --tag python

# 组合使用
cq-knowledge search "错误处理" --tag javascript --limit 3
```

**输出示例**：
```
Found 2 results for 'useEffect'

┌──────────────┬─────────────────────────────────────┬──────────┬─────────────┬─────────┐
│ ID           │ Title                               │ Tags     │ Confidence  │ Updated │
├──────────────┼─────────────────────────────────────┼──────────┼─────────────┼─────────┤
│ a1b2c3d4e5f6 │ React useEffect 无限循环              │ react    │ 0.9         │ 2024-03 │
│              │                                      │ hooks    │             │         │
└──────────────┴─────────────────────────────────────┴──────────┴─────────────┴─────────┘
```

---

### list

列出知识库中的知识单元。

```bash
cq-knowledge list [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--limit` | `-l` | int | ❌ | 20 | 返回结果数量 |
| `--tag` | - | string | ❌ | - | 按标签过滤 |
| `--offset` | - | int | ❌ | 0 | 跳过前 N 条结果 |

**示例**：

```bash
# 列出前 20 条
cq-knowledge list

# 列出特定标签
cq-knowledge list --tag python

# 分页浏览
cq-knowledge list --limit 10 --offset 10
```

**输出示例**：
```
┌──────────────┬─────────────────────┬──────────┬─────────────┬─────────┐
│ ID           │ Title               │ Tags     │ Confidence  │ Updated │
├──────────────┼─────────────────────┼──────────┼─────────────┼─────────┤
│ a1b2c3d4e5f6 │ React useEffect...  │ react    │ 0.9         │ 2024-03 │
│ b2c3d4e5f6g7 │ Python asyncio...   │ python   │ 0.8         │ 2024-03 │
└──────────────┴─────────────────────┴──────────┴─────────────┴─────────┘
```

---

### show

显示知识单元的详细信息。

```bash
cq-knowledge show <知识ID>
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 知识单元 ID（支持短 ID） |

**示例**：

```bash
# 完整 ID
cq-knowledge show a1b2c3d4-e5f6-7890-abcd-ef1234567890

# 短 ID（前几位）
cq-knowledge show a1b2c3d4
```

**输出示例**：
```
╭─ Knowledge Unit Details ─────────────────────────────────────╮
│ Title: React useEffect 无限循环                              │
│ ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890                     │
│ Created: 2024-03-26 10:30                                    │
│ Updated: 2024-03-26 15:45                                    │
│ Source: manual                                               │
│ Verified: No                                                 │
│ Confidence: 0.90                                             │
│ Usage Count: 5                                               │
│ Tags: react, hooks, useEffect                                │
│                                                              │
│ Problem:                                                     │
│ useEffect 依赖数组导致无限循环渲染                            │
│                                                              │
│ Solution:                                                    │
│ 确保依赖数组包含所有外部变量，或使用 useCallback 包裹函数     │
╰──────────────────────────────────────────────────────────────╯

Feedback: 4 helpful, 0 not helpful
```

---

### feedback

为知识单元添加反馈，帮助改进置信度评分。

```bash
cq-knowledge feedback <知识ID> --rating <评分> [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `id` | - | string | ✅ | - | 知识单元 ID |
| `--rating` | `-r` | int | ✅ | - | 评分 1-5 |
| `--comment` | `-c` | string | ❌ | 空 | 评论内容 |

**评分规则**：
- **4-5 分**：有帮助（提升置信度）
- **1-3 分**：没帮助（降低置信度）

**示例**：

```bash
# 正面反馈
cq-knowledge feedback a1b2c3d4 --rating 5 --comment "解决了我的问题！"

# 负面反馈
cq-knowledge feedback a1b2c3d4 --rating 2 --comment "解决方案不完整"
```

**输出示例**：
```
✓ Feedback recorded as helpful
  Rating: 5/5
  Comment: 解决了我的问题！
```

---

### delete

删除知识单元。

```bash
cq-knowledge delete <知识ID> [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `id` | - | string | ✅ | - | 知识单元 ID |
| `--force` | `-f` | flag | ❌ | false | 强制删除，不确认 |

**示例**：

```bash
# 交互式删除（会确认）
cq-knowledge delete a1b2c3d4

# 强制删除（不确认）
cq-knowledge delete a1b2c3d4 --force
```

**输出示例**：
```
Deleting knowledge unit:
  ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Title: React useEffect 无限循环
Are you sure? [y/N]: y
✓ Knowledge unit 'a1b2c3d4' deleted
```

---

### export

导出知识库到 JSON 文件。

```bash
cq-knowledge export [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--output` | `-o` | string | ❌ | backup.json | 输出文件路径 |
| `--feedback` | `-f` | flag | ❌ | false | 包含反馈数据 |

**示例**：

```bash
# 基础导出
cq-knowledge export --output my-backup.json

# 包含反馈数据
cq-knowledge export --output full-backup.json --feedback

# 带时间戳的备份
cq-knowledge export --output "backup-$(date +%Y%m%d).json"
```

**输出示例**：
```
✓ Exported 25 knowledge units to my-backup.json
  Included 12 feedback records
```

---

### import-cmd

从 JSON 文件导入知识库。

```bash
cq-knowledge import-cmd --input <文件路径> [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--input` | `-i` | string | ✅ | - | 输入文件路径 |
| `--skip-existing` | `-s` | flag | ❌ | false | 跳过已存在的知识 |
| `--recalculate` | `-r` | flag | ❌ | false | 导入后重算置信度 |

**示例**：

```bash
# 基础导入
cq-knowledge import-cmd --input backup.json

# 跳过已存在
cq-knowledge import-cmd --input backup.json --skip-existing

# 导入并重算置信度
cq-knowledge import-cmd --input backup.json --recalculate
```

**输出示例**：
```
✓ Import complete:
  Imported: 25 knowledge units
  Skipped: 3 existing units
  Feedback: 12 records
```

---

### recalculate

基于反馈重新计算置信度分数。

```bash
cq-knowledge recalculate [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--id` | `-i` | string | ❌ | - | 特定知识单元 ID |
| `--dry-run` | `-d` | flag | ❌ | false | 预览变化，不应用 |

**示例**：

```bash
# 预览所有变化
cq-knowledge recalculate --dry-run

# 应用所有变化
cq-knowledge recalculate

# 仅重算特定知识
cq-knowledge recalculate --id a1b2c3d4
```

**输出示例**：
```
Recalculating confidence for 25 knowledge unit(s)

┌──────────────┬─────────────────────┬────────┬────────┬────────┬──────────┐
│ ID           │ Title               │ Old    │ New    │ Change │ Feedback │
├──────────────┼─────────────────────┼────────┼────────┼────────┼──────────┤
│ a1b2c3d4e5f6 │ React useEffect...  │ 0.500  │ 0.900  │ +0.400 │ +4/-0    │
│ b2c3d4e5f6g7 │ Python asyncio...  │ 0.600  │ 0.400  │ -0.200 │ +2/-3    │
└──────────────┴─────────────────────┴────────┴────────┴────────┴──────────┘

✓ Updated confidence for 2 knowledge unit(s)
```

---

### serve

启动 REST API 服务器。

```bash
cq-knowledge serve [选项]
```

| 参数 | 简写 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `--host` | `-h` | string | ❌ | 127.0.0.1 | 绑定地址 |
| `--port` | `-p` | int | ❌ | 8000 | 绑定端口 |
| `--reload` | `-r` | flag | ❌ | false | 自动重载 |

**示例**：

```bash
# 默认配置
cq-knowledge serve

# 自定义地址和端口
cq-knowledge serve --host 0.0.0.0 --port 8080

# 开发模式（自动重载）
cq-knowledge serve --reload
```

**输出示例**：
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `CQ_DB_PATH` | 数据库文件路径 | `~/.cq/knowledge.db` |
| `CQ_LOG_LEVEL` | 日志级别 | `INFO` |

**示例**：

```bash
# 自定义数据库位置
export CQ_DB_PATH=/custom/path/knowledge.db
cq-knowledge init

# 启用调试日志
export CQ_LOG_LEVEL=DEBUG
cq-knowledge search "test"
```

---

## 退出代码

| 代码 | 说明 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 参数错误 |

---

## 相关文档

- [快速开始](getting-started.md)
- [MCP 集成指南](mcp-integration.md)
- [API 参考](api-reference.md)
- [常见问题](faq.md)
