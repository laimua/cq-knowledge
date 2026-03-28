# Cq MCP 集成指南

本指南介绍如何将 Cq 与支持 MCP (Model Context Protocol) 的 AI 编码工具集成。

## 什么是 MCP？

MCP (Model Context Protocol) 是一个开放协议，允许 AI 助手与外部工具和数据源通信。Cq 通过 MCP 插件可以将知识库功能暴露给 AI 编码代理。

## 支持的工具

- ✅ Claude Code
- ✅ Cline (Cursor)
- ✅ 任何支持 MCP 协议的工具

## Claude Code 集成

### 安装步骤

#### 1. 安装 Cq

```bash
pip install cq-knowledge
```

#### 2. 配置 MCP 服务器

找到 Claude Code 配置文件：

- **macOS/Linux**: `~/.claude/config.json`
- **Windows**: `%USERPROFILE%\.claude\config.json`

在配置文件中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

#### 3. 重启 Claude Code

完全退出 Claude Code 并重新启动。

#### 4. 验证安装

在 Claude Code 对话中输入：

```
列出可用的 MCP 工具
```

你应该看到 Cq 提供的工具。

### 可用工具

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `cq_search` | 搜索知识库 | `query`, `limit?`, `tag?` |
| `cq_add` | 添加知识单元 | `title`, `problem`, `solution`, `tags?`, `confidence?` |
| `cq_show` | 查看知识详情 | `id` |
| `cq_list` | 列出知识 | `limit?`, `tag?` |
| `cq_feedback` | 添加反馈 | `ku_id`, `rating`, `comment?` |

### 使用示例

#### 搜索知识

> 请搜索关于 Python asyncio 的知识

> 找找 React hooks 相关的解决方案

> 搜索标签为 "git" 的知识

#### 添加知识

> 添加一条知识：
> - 标题：解决 Git 合并冲突
> - 问题：合并代码时出现冲突
> - 解决方案：使用 git mergetool 或手动解决
> - 标签：git, version-control

> 我刚解决了 "Docker 容器无法访问宿主机服务" 的问题，把解决方案添加到知识库：
> 问题：容器内无法访问 localhost 上的服务
> 解决方案：使用 host.docker.internal 代替 localhost

#### 查看详情

> 显示知识 ID 为 abc123 的详细信息

#### 列出知识

> 列出所有标签为 "python" 的知识

> 显示最近添加的 10 条知识

#### 添加反馈

> 知识 abc123 帮到了我，给它 5 分好评

> 知识 def456 的解决方案不对，给它 2 分

### 完整工作流示例

```
用户: 我遇到了 React useEffect 无限循环的问题

Claude: 让我搜索一下相关知识...

[使用 cq_search 工具搜索 "useEffect 循环"]

Claude: 我找到了相关知识：
1. React useEffect 无限循环 - 确保依赖数组包含所有外部变量

根据知识库，你应该检查 useEffect 的依赖数组是否包含所有外部变量...

用户: 太好了，解决了！给这条知识点个赞

Claude: [使用 cq_feedback 工具，ku_id=xxx, rating=5]
已记录您的反馈，谢谢！
```

## Cline (Cursor) 集成

### 配置步骤

#### 1. 安装 Cq

```bash
pip install cq-knowledge
```

#### 2. 配置 MCP 服务器

找到 Cline 配置文件：

- **macOS**: `~/Library/Application Support/Cline/config.json`
- **Windows**: `%APPDATA%\Cline\config.json`
- **Linux**: `~/.config/Cline/config.json`

添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

#### 3. 重启 Cursor IDE

#### 4. 使用

在 Cline 对话中自然语言调用，使用方式与 Claude Code 类似。

## 其他 MCP 客户端

任何支持 MCP 协议的工具都可以集成 Cq。基本步骤：

1. 安装 Cq: `pip install cq-knowledge`
2. 配置 MCP 服务器，命令为 `cq-knowledge-mcp`
3. 重启应用

## MCP 工具详细说明

### cq_search

搜索知识库中的知识单元。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `limit` | number | ❌ | 返回结果数量 (1-50, 默认 5) |
| `tag` | string | ❌ | 按标签过滤 |

**示例**：

```json
{
  "query": "useEffect 循环",
  "limit": 10,
  "tag": "react"
}
```

**返回**：

```markdown
Found 2 results for 'useEffect 循环':

## 1. React useEffect 无限循环 ✓
**ID:** a1b2c3d4-e5f6-7890-abcd-ef1234567890
**Tags:** react, hooks
**Confidence:** 0.90 | **Rank:** 1.50

**Problem:**
useEffect 依赖数组导致无限循环渲染...

**Solution:**
确保依赖数组包含所有外部变量...
```

### cq_add

添加新的知识单元。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 知识标题 |
| `problem` | string | ✅ | 问题描述 |
| `solution` | string | ✅ | 解决方案 |
| `tags` | string[] | ❌ | 标签列表 |
| `confidence` | number | ❌ | 置信度 (0-1, 默认 0.5) |

**示例**：

```json
{
  "title": "解决 CORS 错误",
  "problem": "浏览器跨域请求被阻止",
  "solution": "在后端设置 Access-Control-Allow-Origin 响应头",
  "tags": ["web", "cors", "javascript"],
  "confidence": 0.9
}
```

**返回**：

```markdown
✓ Knowledge unit added successfully

**ID:** a1b2c3d4-e5f6-7890-abcd-ef1234567890
**Title:** 解决 CORS 错误
```

### cq_show

获取知识单元详情。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 知识单元 ID |

**示例**：

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**返回**：

```markdown
# React useEffect 无限循环 ✓

**ID:** a1b2c3d4-e5f6-7890-abcd-ef1234567890
**Source:** claude_code
**Verified:** No
**Confidence:** 0.90
**Usage Count:** 5
**Tags:** react, hooks
**Created:** 2024-03-26 10:30:00
**Updated:** 2024-03-26 15:45:00

## Problem
useEffect 依赖数组导致无限循环渲染

## Solution
确保依赖数组包含所有外部变量，或使用 useCallback 包裹函数

---

**Feedback:** 4 helpful, 0 not helpful (total: 4)
```

### cq_list

列出知识单元。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | number | ❌ | 返回结果数量 (1-100, 默认 20) |
| `tag` | string | ❌ | 按标签过滤 |

**示例**：

```json
{
  "limit": 10,
  "tag": "python"
}
```

**返回**：

```markdown
Found 5 knowledge unit(s):

## 1. Python asyncio 最佳实践 ✓
**ID:** a1b2c3d4-e5f6-7890-abcd-ef1234567890
**Tags:** python, asyncio
**Confidence:** 0.90
**Updated:** 2024-03-26
...
```

### cq_feedback

为知识单元添加反馈。

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ku_id` | string | ✅ | 知识单元 ID |
| `rating` | number | ✅ | 评分 1-5 |
| `comment` | string | ❌ | 评论内容 |

**评分规则**：
- **4-5 分**：有帮助（提升置信度）
- **1-3 分**：没帮助（降低置信度）

**示例**：

```json
{
  "ku_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "rating": 5,
  "comment": "完美解决了我的问题！"
}
```

**返回**：

```markdown
✓ Feedback recorded as helpful

**Knowledge Unit:** React useEffect 无限循环
**Rating:** 5/5
```

## 故障排除

### 问题：工具不可见

**症状**：在 Claude Code 中看不到 Cq 工具

**解决方案**：

1. 确认已安装：
```bash
pip show cq-knowledge
```

2. 检查配置：
```bash
cat ~/.claude/config.json
```

3. 测试 MCP 服务器：
```bash
cq-knowledge-mcp
```

4. 重启 Claude Code（完全退出）

### 问题：工具调用失败

**症状**：调用工具时报错

**解决方案**：

1. 检查日志：
```bash
# macOS/Linux
tail -f ~/.claude/logs/mcp.log

# Windows
type %USERPROFILE%\.claude\logs\mcp.log
```

2. 确认数据库已初始化：
```bash
cq-knowledge init
```

### 问题：搜索结果为空

**症状**：搜索返回 "No results found"

**解决方案**：

1. 确认知识库有数据：
```bash
cq-knowledge list
```

2. 尝试不同的关键词

3. 不使用标签过滤进行搜索

## 高级配置

### 自定义数据库路径

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp",
      "env": {
        "CQ_DB_PATH": "/custom/path/knowledge.db"
      }
    }
  }
}
```

### 启用调试日志

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp",
      "env": {
        "CQ_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## 最佳实践

1. **添加知识时**：提供清晰的标题和详细的问题描述
2. **搜索时**：使用具体的关键词，适当使用标签过滤
3. **反馈时**：诚实地评分，帮助改进知识库质量
4. **定期维护**：使用 CLI 工具导出备份，清理过时知识

## 相关文档

- [快速开始](getting-started.md)
- [CLI 命令参考](cli-reference.md)
- [API 参考](api-reference.md)
- [常见问题](faq.md)
