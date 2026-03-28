# Cq 快速开始指南

欢迎使用 Cq！本指南将在 5 分钟内带你完成安装和基本使用。

## 前置要求

- Python 3.10 或更高版本
- pip 或 uv 包管理器

## 第一步：安装

### 方法 A：使用 pip（推荐）

```bash
pip install cq-knowledge
```

### 方法 B：使用 uvx（更快）

```bash
uvx --from cq-knowledge cq-knowledge --help
```

### 验证安装

```bash
cq-knowledge --version
```

你应该看到版本号输出。

## 第二步：初始化知识库

```bash
cq-knowledge init
```

这将在 `~/.cq/` 目录创建 SQLite 数据库文件。

输出示例：
```
✓ Knowledge base initialized at /home/user/.cq/knowledge.db
```

## 第三步：添加知识

### 基础用法

```bash
cq-knowledge add \
  --title "解决 React useEffect 无限循环" \
  --problem "useEffect 依赖数组导致无限循环渲染" \
  --solution "确保依赖数组包含所有外部变量，或使用 useCallback 包裹函数" \
  --tags "react,hooks,useEffect"
```

### 带置信度的添加

```bash
cq-knowledge add \
  --title "Python asyncio 最佳实践" \
  --problem "asyncio 任务不执行" \
  --solution "使用 asyncio.run() 而非手动创建事件循环" \
  --tags "python,asyncio" \
  --confidence 0.9
```

## 第四步：搜索知识

### 关键词搜索

```bash
cq-knowledge search "useEffect"
```

### 带标签过滤

```bash
cq-knowledge search "异步" --tag python
```

### 限制结果数量

```bash
cq-knowledge search "循环" --limit 5
```

## 第五步：查看和管理

### 列出所有知识

```bash
cq-knowledge list
```

### 查看特定知识详情

```bash
cq-knowledge show <知识ID>
```

### 添加反馈

```bash
cq-knowledge feedback <知识ID> --rating 5 --comment "解决了我的问题！"
```

评分规则：
- 4-5 分：有帮助
- 1-3 分：没帮助

## 第六步：（可选）Claude Code 集成

### 配置步骤

1. 找到 Claude Code 配置文件：
   - macOS/Linux: `~/.claude/config.json`
   - Windows: `%USERPROFILE%\.claude\config.json`

2. 添加 MCP 服务器配置：

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

### 在 Claude Code 中使用

在对话中直接使用自然语言：

> 请搜索关于 React hooks 的知识

> 添加一条知识：标题是"解决 Git 冲突"，问题是"合并代码时出现冲突"，解决方案是"使用 git mergetool"

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `cq-knowledge init` | 初始化知识库 |
| `cq-knowledge add -t "标题" -p "问题" -s "解决方案"` | 添加知识 |
| `cq-knowledge search "关键词"` | 搜索知识 |
| `cq-knowledge list` | 列出所有知识 |
| `cq-knowledge show <ID>` | 查看详情 |
| `cq-knowledge feedback <ID> --rating 5` | 添加反馈 |
| `cq-knowledge export --output backup.json` | 导出备份 |
| `cq-knowledge import-cmd --input backup.json` | 导入备份 |

## 下一步

- 查看 [CLI 命令详解](cli-reference.md) 了解所有命令
- 查看 [MCP 集成指南](mcp-integration.md) 深入了解 MCP 集成
- 查看 [API 参考](api-reference.md) 了解 REST API 使用
- 查看 [FAQ](faq.md) 解答常见问题

## 遇到问题？

1. 检查 Python 版本：`python --version`
2. 检查安装状态：`pip show cq-knowledge`
3. 查看错误日志：`~/.cq/logs/`（如果存在）
4. 在 GitHub 提交 issue

祝你使用愉快！
