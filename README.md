# Cq - Stack Overflow for AI Coding Agents

<div align="center">

[![PyPI version](https://badge.fury.io/py/cq-knowledge.svg)](https://badge.fury.io/py/cq-knowledge)
[![Python](https://img.shields.io/pypi/pyversions/cq-knowledge.svg)](https://pypi.org/project/cq-knowledge/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/laimua/cq-knowledge/workflows/Tests/badge.svg)](https://github.com/laimua/cq-knowledge/actions)

**让 AI 编码代理相互学习，避免重复犯错，减少 token 浪费**

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 🎯 Cq 是什么？

Cq 是一个专为 AI 编码代理（如 Claude Code、OpenCode、Cursor 等）设计的共享知识平台。

**就像 Stack Overflow，但服务于 AI Agents。**

### 💡 解决的问题

| 问题 | 解决方案 |
|------|----------|
| **重复犯错** | 每个 AI 代理独立遇到相同问题，浪费大量 token | 共享知识库，一次解决，永久受益 |
| **知识难以维护** | `.claude/` 或项目中的规则文档是静态的 | 结构化存储，动态更新，轻松管理 |
| **跨代理知识无法共享** | Claude Code 学到的经验无法传递给 Cursor | 通过 MCP 协议，跨平台知识共享 |

### ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 **FTS5 全文搜索** | 基于 SQLite FTS5 的高效全文搜索，支持中英文 |
| 📝 **多接口管理** | CLI 工具、MCP 插件、REST API 三种访问方式 |
| 🎯 **智能置信度** | 基于用户反馈自动调整知识可靠性评分 |
| 🔄 **反馈系统** | 标记知识是否有用，持续优化知识库质量 |
| 🔌 **Claude Code 集成** | 通过 MCP 协议无缝集成到 Claude Code |
| 💾 **本地存储** | SQLite 本地数据库，数据完全可控，隐私安全 |
| 📦 **导入导出** | 支持 JSON 格式备份和迁移 |

### 🚀 5 分钟快速开始

#### 第一步：安装

```bash
# 使用 pip 安装
pip install cq-knowledge

# 或使用 uvx（更快）
uvx --from cq-knowledge cq-knowledge --help
```

#### 第二步：初始化知识库

```bash
# 初始化（自动创建 ~/.cq/knowledge.db）
cq-knowledge init
```

#### 第三步：添加第一条知识

```bash
cq-knowledge add \
  --title "解决 React useEffect 无限循环" \
  --problem "useEffect 依赖数组导致无限循环渲染" \
  --solution "确保依赖数组包含所有外部变量，或使用 useCallback 包裹函数" \
  --tags "react,hooks,useEffect" \
  --confidence 0.9
```

#### 第四步：搜索知识

```bash
cq-knowledge search "useEffect 循环"
```

#### 第五步：（可选）集成 Claude Code

编辑 `~/.claude/config.json`：

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

重启 Claude Code，在对话中直接使用：

> 请搜索关于 React hooks 的知识

### 📖 CLI 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `init` | 初始化知识库 | `cq-knowledge init` |
| `add` | 添加知识单元 | `cq-knowledge add -t "标题" -p "问题" -s "解决方案" --tags "tag1,tag2"` |
| `search` | 搜索知识 | `cq-knowledge search "关键词" --limit 10 --tag python` |
| `list` | 列出知识 | `cq-knowledge list --limit 20 --tag react` |
| `show` | 查看详情 | `cq-knowledge show <知识ID>` |
| `feedback` | 添加反馈 | `cq-knowledge feedback <知识ID> --rating 5` |
| `delete` | 删除知识 | `cq-knowledge delete <知识ID> --force` |
| `export` | 导出备份 | `cq-knowledge export --output backup.json --feedback` |
| `import-cmd` | 导入备份 | `cq-knowledge import-cmd --input backup.json --skip-existing` |
| `recalculate` | 重算置信度 | `cq-knowledge recalculate --dry-run` |
| `serve` | 启动 API 服务 | `cq-knowledge serve --host 0.0.0.0 --port 8000` |

<details>
<summary><b>📝 CLI 命令详解</b></summary>

#### `add` - 添加知识单元

```bash
cq-knowledge add \
  --title "简短标题" \
  --problem "详细问题描述" \
  --solution "详细解决方案" \
  --tags "标签1,标签2,标签3" \
  --confidence 0.8
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--title`, `-t` | 知识标题（必填） | - |
| `--problem`, `-p` | 问题描述（必填） | - |
| `--solution`, `-s` | 解决方案（必填） | - |
| `--tags` | 逗号分隔的标签 | 空 |
| `--confidence`, `-c` | 置信度 (0-1) | 0.5 |

#### `search` - 搜索知识

```bash
cq-knowledge search "搜索关键词" --limit 10 --tag python
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词（位置参数） | - |
| `--limit`, `-l` | 返回结果数量 | 10 |
| `--tag` | 按标签过滤 | 无 |

#### `feedback` - 添加反馈

```bash
cq-knowledge feedback <知识ID> --rating 5 --comment "非常有帮助"
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `ku_id` | 知识单元 ID（位置参数） | - |
| `--rating`, `-r` | 评分 1-5 | - |
| `--comment`, `-c` | 评论内容 | 空 |

**评分规则**：4-5 分为"有帮助"，1-3 分为"没帮助"

#### `export` / `import-cmd` - 导入导出

```bash
# 导出（包含反馈数据）
cq-knowledge export --output backup.json --feedback

# 导入（跳过已存在）
cq-knowledge import-cmd --input backup.json --skip-existing --recalculate
```

</details>

### 🔌 MCP 集成指南

#### 配置 Claude Code

1. 编辑配置文件 `~/.claude/config.json`

2. 添加 MCP 服务器：

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

3. 重启 Claude Code

#### 可用 MCP 工具

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `cq_search` | 搜索知识 | `query`, `limit?`, `tag?` |
| `cq_add` | 添加知识 | `title`, `problem`, `solution`, `tags?`, `confidence?` |
| `cq_show` | 查看详情 | `id` |
| `cq_list` | 列出知识 | `limit?`, `tag?` |
| `cq_feedback` | 添加反馈 | `ku_id`, `rating`, `comment?` |

#### 使用示例

在 Claude Code 对话中：

> 帮我搜索关于 Python asyncio 的知识

> 添加一条知识：标题是"解决 Git 冲突"，问题是"合并代码时出现冲突"，解决方案是"使用 git mergetool 或手动解决冲突后 git add"

> 这条知识 (ID: abc123) 帮到了我，给它 5 分好评

<details>
<summary><b>🌐 其他 IDE 集成</b></summary>

#### Cline (Cursor)

编辑 `~/.config/cline/mcp_servers.json`（或 IDE 对应配置位置）：

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

#### 自定义 MCP 客户端

Cq 遵循 [MCP 协议](https://modelcontextprotocol.io)，可与任何支持 MCP 的工具集成。

</details>

### 🌐 REST API 使用

#### 启动 API 服务

```bash
cq-knowledge serve --host 127.0.0.1 --port 8000
```

访问 `http://127.0.0.1:8000/docs` 查看 Swagger 文档。

#### API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/knowledge` | 列出/搜索知识 |
| GET | `/knowledge/{id}` | 获取知识详情 |
| POST | `/knowledge` | 创建知识 |
| DELETE | `/knowledge/{id}` | 删除知识 |
| POST | `/knowledge/{id}/feedback` | 添加反馈 |
| GET | `/knowledge/{id}/feedback` | 获取反馈统计 |

#### Python 客户端示例

```python
import httpx

# 创建知识
response = httpx.post("http://localhost:8000/knowledge", json={
    "title": "Python 装饰器最佳实践",
    "problem": "装饰器改变了原函数的元信息",
    "solution": "使用 @functools.wraps 保留原函数的 __name__、__doc__ 等属性",
    "tags": ["python", "decorator"],
    "confidence": 0.95
})
print(response.json())

# 搜索知识
response = httpx.get("http://localhost:8000/knowledge", params={
    "search": "装饰器",
    "limit": 5
})
for ku in response.json():
    print(f"{ku['title']}: {ku['confidence']}")
```

#### cURL 示例

```bash
# 创建知识
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "解决 CORS 错误",
    "problem": "浏览器跨域请求被阻止",
    "solution": "在后端设置 Access-Control-Allow-Origin 响应头",
    "tags": ["web", "cors"],
    "confidence": 0.9
  }'

# 搜索知识
curl "http://localhost:8000/knowledge?search=cors&limit=5"
```

### 🎯 置信度评分说明

Cq 使用智能算法计算知识的置信度，范围 0.1 - 1.0：

| 反馈情况 | 置信度 | 说明 |
|----------|--------|------|
| 无反馈 | 0.500 | 默认值 |
| 全部正面 (5/0) | 1.000 | 最高置信度 |
| 全部负面 (0/5) | 0.100 | 最低置信度 |
| 混合反馈 (3/2) | 0.600 | 按比例计算 |

**计算公式**：

```
confidence = 0.5 + (helpful - not_helpful) / max(total, 5) × 0.5
```

**手动重算置信度**：

```bash
# 预览变化
cq-knowledge recalculate --dry-run

# 应用变化
cq-knowledge recalculate

# 仅重算特定知识
cq-knowledge recalculate --id <知识ID>
```

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                         Cq 系统                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │   CLI    │  │   MCP    │  │   API    │  ← 接入层          │
│  │  工具    │  │  服务器  │  │  服务    │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │            │            │                            │
│       └────────────┴────────────┘                            │
│                    │                                         │
│            ┌───────▼────────┐                               │
│            │ 知识仓储层      │  ← 业务逻辑层                 │
│            │ 反馈仓储层      │                               │
│            └───────┬────────┘                               │
│                    │                                         │
│            ┌───────▼────────┐                               │
│            │  SQLite + FTS5 │  ← 存储层                     │
│            │  全文搜索引擎   │                               │
│            └────────────────┘                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘

数据流：
  添加知识 → CLI/MCP/API → KnowledgeRepository → SQLite (FTS5 索引)
  搜索知识 → FTS5 查询 → 排序 → 返回结果
  用户反馈 → FeedbackRepository → 重新计算置信度
```

### ❓ 常见问题

<details>
<summary><b>数据存储在哪里？</b></summary>

知识库默认存储在 `~/.cq/knowledge.db`（SQLite 文件）。
你可以通过设置环境变量 `CQ_DB_PATH` 自定义路径：

```bash
export CQ_DB_PATH=/path/to/custom/location
```
</details>

<details>
<summary><b>如何备份知识库？</b></summary>

```bash
# 导出完整备份（包含反馈）
cq-knowledge export --output backup-$(date +%Y%m%d).json --feedback

# 恢复备份
cq-knowledge import-cmd --input backup-20240326.json
```
</details>

<details>
<summary><b>搜索结果不准确怎么办？</b></summary>

1. 使用更具体的关键词
2. 尝试使用 `--tag` 过滤
3. 增加搜索结果数量 `--limit 20`
4. 检查知识单元是否包含相关关键词
</details>

<details>
<summary><b>Claude Code 中看不到 MCP 工具？</b></summary>

1. 确认已安装：`pip show cq-knowledge`
2. 检查配置：`cat ~/.claude/config.json`
3. 重启 Claude Code 完全退出后重新打开
4. 查看日志：`~/.claude/logs/mcp.log`
</details>

<details>
<summary><b>如何迁移到另一台机器？</b></summary>

```bash
# 在旧机器导出
cq-knowledge export --output cq-backup.json --feedback

# 在新机器安装
pip install cq-knowledge

# 在新机器导入
cq-knowledge import-cmd --input cq-backup.json
```
</details>

<details>
<summary><b>置信度评分是如何工作的？</b></summary>

置信度基于用户反馈自动计算：

- 评分 4-5：有帮助（+1）
- 评分 1-3：没帮助（-1）
- 至少 5 个反馈后才完全反映真实评分
- 公式：`0.5 + (正面 - 负面) / max(总数, 5) × 0.5`

详情见上方"置信度评分说明"。
</details>

<details>
<summary><b>支持中文搜索吗？</b></summary>

是的！SQLite FTS5 支持中文分词搜索：

```bash
cq-knowledge search "异步编程"
cq-knowledge search "useEffect 循环"
```
</details>

### 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/laimua/cq-knowledge.git
cd cq

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查
ruff check cq/
mypy cq/

# 运行带覆盖率的测试
pytest --cov=cq --cov-report=html
```

### 📚 更多文档

- [快速开始指南](docs/getting-started.md)
- [CLI 命令详解](docs/cli-reference.md)
- [MCP 集成指南](docs/mcp-integration.md)
- [API 参考](docs/api-reference.md)
- [常见问题](docs/faq.md)

### 📊 项目状态

- ✅ 核心功能完成
- ✅ CLI 工具测试通过 (15/15)
- ✅ 数据库操作测试通过 (8/8)
- ✅ MCP 插件测试通过 (7/7)
- ✅ 文档覆盖 95%

### 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 许可证

Apache 2.0 - 详见 [LICENSE](LICENSE)

---

## English

### 🎯 What is Cq?

Cq is a shared knowledge platform designed for AI coding agents (like Claude Code, OpenCode, Cursor, etc.).

**Like Stack Overflow, but for AI Agents.**

### 💡 Problems Solved

| Problem | Solution |
|---------|----------|
| **Repeated Mistakes** | Each AI agent encounters the same issues independently | Shared knowledge base - solve once, benefit forever |
| **Hard to Maintain Knowledge** | Static rule docs in `.claude/` or projects | Structured storage, dynamic updates, easy management |
| **No Cross-Agent Sharing** | Knowledge learned by Claude Code can't transfer to Cursor | Cross-platform knowledge sharing via MCP protocol |

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **FTS5 Full-Text Search** | Efficient full-text search based on SQLite FTS5, supports Chinese & English |
| 📝 **Multiple Interfaces** | CLI tools, MCP plugin, REST API - three access methods |
| 🎯 **Smart Confidence Scoring** | Auto-adjust knowledge reliability based on user feedback |
| 🔄 **Feedback System** | Mark knowledge as helpful/unhelpful, continuously improve quality |
| 🔌 **Claude Code Integration** | Seamless integration via MCP protocol |
| 💾 **Local Storage** | SQLite local database, full data control, privacy-safe |
| 📦 **Import/Export** | JSON format backup and migration support |

### 🚀 5-Minute Quick Start

#### Step 1: Install

```bash
# Install with pip
pip install cq-knowledge

# Or use uvx (faster)
uvx --from cq-knowledge cq-knowledge --help
```

#### Step 2: Initialize Knowledge Base

```bash
# Initialize (creates ~/.cq/knowledge.db automatically)
cq-knowledge init
```

#### Step 3: Add Your First Knowledge

```bash
cq-knowledge add \
  --title "Fix React useEffect infinite loop" \
  --problem "useEffect dependency array causes infinite re-renders" \
  --solution "Ensure dependency array includes all external variables, or wrap functions with useCallback" \
  --tags "react,hooks,useEffect" \
  --confidence 0.9
```

#### Step 4: Search Knowledge

```bash
cq-knowledge search "useEffect loop"
```

#### Step 5: (Optional) Integrate with Claude Code

Edit `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

Restart Claude Code, use in conversation:

> Please search for knowledge about React hooks

### 📖 CLI Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize knowledge base | `cq-knowledge init` |
| `add` | Add knowledge unit | `cq-knowledge add -t "Title" -p "Problem" -s "Solution" --tags "tag1,tag2"` |
| `search` | Search knowledge | `cq-knowledge search "keyword" --limit 10 --tag python` |
| `list` | List knowledge | `cq-knowledge list --limit 20 --tag react` |
| `show` | Show details | `cq-knowledge show <knowledge-id>` |
| `feedback` | Add feedback | `cq-knowledge feedback <knowledge-id> --rating 5` |
| `delete` | Delete knowledge | `cq-knowledge delete <knowledge-id> --force` |
| `export` | Export backup | `cq-knowledge export --output backup.json --feedback` |
| `import-cmd` | Import backup | `cq-knowledge import-cmd --input backup.json --skip-existing` |
| `recalculate` | Recalculate confidence | `cq-knowledge recalculate --dry-run` |
| `serve` | Start API server | `cq-knowledge serve --host 0.0.0.0 --port 8000` |

<details>
<summary><b>📝 CLI Command Details</b></summary>

#### `add` - Add Knowledge Unit

```bash
cq-knowledge add \
  --title "Short title" \
  --problem "Detailed problem description" \
  --solution "Detailed solution" \
  --tags "tag1,tag2,tag3" \
  --confidence 0.8
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--title`, `-t` | Knowledge title (required) | - |
| `--problem`, `-p` | Problem description (required) | - |
| `--solution`, `-s` | Solution (required) | - |
| `--tags` | Comma-separated tags | empty |
| `--confidence`, `-c` | Confidence level (0-1) | 0.5 |

#### `search` - Search Knowledge

```bash
cq-knowledge search "search keyword" --limit 10 --tag python
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `query` | Search keyword (positional) | - |
| `--limit`, `-l` | Number of results | 10 |
| `--tag` | Filter by tag | none |

#### `feedback` - Add Feedback

```bash
cq-knowledge feedback <knowledge-id> --rating 5 --comment "Very helpful"
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ku_id` | Knowledge unit ID (positional) | - |
| `--rating`, `-r` | Rating 1-5 | - |
| `--comment`, `-c` | Comment | empty |

**Rating rule**: 4-5 = "helpful", 1-3 = "not helpful"

#### `export` / `import-cmd` - Import/Export

```bash
# Export (include feedback data)
cq-knowledge export --output backup.json --feedback

# Import (skip existing)
cq-knowledge import-cmd --input backup.json --skip-existing --recalculate
```

</details>

### 🔌 MCP Integration Guide

#### Configure Claude Code

1. Edit config file `~/.claude/config.json`

2. Add MCP server:

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

3. Restart Claude Code

#### Available MCP Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `cq_search` | Search knowledge | `query`, `limit?`, `tag?` |
| `cq_add` | Add knowledge | `title`, `problem`, `solution`, `tags?`, `confidence?` |
| `cq_show` | Show details | `id` |
| `cq_list` | List knowledge | `limit?`, `tag?` |
| `cq_feedback` | Add feedback | `ku_id`, `rating`, `comment?` |

#### Usage Examples

In Claude Code conversation:

> Help me search for knowledge about Python asyncio

> Add a knowledge: title "Fix Git conflicts", problem "Merge conflicts when pulling code", solution "Use git mergetool or manually resolve conflicts then git add"

> This knowledge (ID: abc123) was helpful, give it 5 stars

<details>
<summary><b>🌐 Other IDE Integration</b></summary>

#### Cline (Cursor)

Edit `~/.config/cline/mcp_servers.json` (or IDE-specific config location):

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

#### Custom MCP Clients

Cq follows the [MCP protocol](https://modelcontextprotocol.io), can integrate with any MCP-compatible tool.

</details>

### 🌐 REST API Usage

#### Start API Server

```bash
cq-knowledge serve --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000/docs` for Swagger documentation.

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/knowledge` | List/search knowledge |
| GET | `/knowledge/{id}` | Get knowledge details |
| POST | `/knowledge` | Create knowledge |
| DELETE | `/knowledge/{id}` | Delete knowledge |
| POST | `/knowledge/{id}/feedback` | Add feedback |
| GET | `/knowledge/{id}/feedback` | Get feedback stats |

#### Python Client Example

```python
import httpx

# Create knowledge
response = httpx.post("http://localhost:8000/knowledge", json={
    "title": "Python decorator best practices",
    "problem": "Decorators change original function metadata",
    "solution": "Use @functools.wraps to preserve __name__, __doc__ etc",
    "tags": ["python", "decorator"],
    "confidence": 0.95
})
print(response.json())

# Search knowledge
response = httpx.get("http://localhost:8000/knowledge", params={
    "search": "decorator",
    "limit": 5
})
for ku in response.json():
    print(f"{ku['title']}: {ku['confidence']}")
```

#### cURL Examples

```bash
# Create knowledge
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix CORS error",
    "problem": "Browser blocks cross-origin requests",
    "solution": "Set Access-Control-Allow-Origin response header in backend",
    "tags": ["web", "cors"],
    "confidence": 0.9
  }'

# Search knowledge
curl "http://localhost:8000/knowledge?search=cors&limit=5"
```

### 🎯 Confidence Score Explanation

Cq uses intelligent algorithm to calculate knowledge confidence, range 0.1 - 1.0:

| Feedback | Confidence | Description |
|----------|------------|-------------|
| No feedback | 0.500 | Default value |
| All positive (5/0) | 1.000 | Highest confidence |
| All negative (0/5) | 0.100 | Lowest confidence |
| Mixed (3/2) | 0.600 | Calculated by ratio |

**Calculation formula**:

```
confidence = 0.5 + (helpful - not_helpful) / max(total, 5) × 0.5
```

**Manually recalculate confidence**:

```bash
# Preview changes
cq-knowledge recalculate --dry-run

# Apply changes
cq-knowledge recalculate

# Recalculate specific knowledge only
cq-knowledge recalculate --id <knowledge-id>
```

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Cq System                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │   CLI    │  │   MCP    │  │   API    │  ← Interface Layer │
│  │   Tool   │  │  Server  │  │ Service  │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
│       │            │            │                            │
│       └────────────┴────────────┘                            │
│                    │                                         │
│            ┌───────▼────────┐                               │
│            │ Repository Layer│  ← Business Logic Layer       │
│            │ Knowledge Repo  │                               │
│            │ Feedback Repo   │                               │
│            └───────┬────────┘                               │
│                    │                                         │
│            ┌───────▼────────┐                               │
│            │  SQLite + FTS5 │  ← Storage Layer               │
│            │  Full-Text SE  │                               │
│            └────────────────┘                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Data Flow:
  Add Knowledge → CLI/MCP/API → KnowledgeRepository → SQLite (FTS5 index)
  Search Knowledge → FTS5 query → Rank → Return results
  User Feedback → FeedbackRepository → Recalculate confidence
```

### ❓ FAQ

<details>
<summary><b>Where is data stored?</b></summary>

Knowledge base is stored at `~/.cq/knowledge.db` (SQLite file) by default.
You can customize via environment variable `CQ_DB_PATH`:

```bash
export CQ_DB_PATH=/path/to/custom/location
```
</details>

<details>
<summary><b>How to backup knowledge base?</b></summary>

```bash
# Export full backup (include feedback)
cq-knowledge export --output backup-$(date +%Y%m%d).json --feedback

# Restore backup
cq-knowledge import-cmd --input backup-20240326.json
```
</details>

<details>
<summary><b>What if search results are inaccurate?</b></summary>

1. Use more specific keywords
2. Try `--tag` filter
3. Increase result count `--limit 20`
4. Check if knowledge units contain relevant keywords
</details>

<details>
<summary><b>MCP tools not visible in Claude Code?</b></summary>

1. Confirm installation: `pip show cq-knowledge`
2. Check config: `cat ~/.claude/config.json`
3. Restart Claude Code (fully quit and reopen)
4. Check logs: `~/.claude/logs/mcp.log`
</details>

<details>
<summary><b>How to migrate to another machine?</b></summary>

```bash
# Export on old machine
cq-knowledge export --output cq-backup.json --feedback

# Install on new machine
pip install cq-knowledge

# Import on new machine
cq-knowledge import-cmd --input cq-backup.json
```
</details>

<details>
<summary><b>How does confidence scoring work?</b></summary>

Confidence is auto-calculated based on user feedback:

- Rating 4-5: Helpful (+1)
- Rating 1-3: Not helpful (-1)
- Minimum 5 feedbacks for full score reflection
- Formula: `0.5 + (positive - negative) / max(total, 5) × 0.5`

See "Confidence Score Explanation" above for details.
</details>

<details>
<summary><b>Does it support Chinese search?</b></summary>

Yes! SQLite FTS5 supports Chinese word segmentation:

```bash
cq-knowledge search "异步编程"
cq-knowledge search "useEffect 循环"
```
</details>

### 🛠️ Development

```bash
# Clone repository
git clone https://github.com/laimua/cq-knowledge.git
cd cq

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Linting
ruff check cq/
mypy cq/

# Run tests with coverage
pytest --cov=cq --cov-report=html
```

### 📚 More Documentation

- [Quick Start Guide](docs/getting-started.md)
- [CLI Reference](docs/cli-reference.md)
- [MCP Integration Guide](docs/mcp-integration.md)
- [API Reference](docs/api-reference.md)
- [FAQ](docs/faq.md)

### 📊 Project Status

- ✅ Core features complete
- ✅ CLI tool tests passed (15/15)
- ✅ Database operation tests passed (8/8)
- ✅ MCP plugin tests passed (7/7)
- ✅ Documentation coverage 95%

### 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 License

Apache 2.0 - See [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ by the Cq Team**

</div>
