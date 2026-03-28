# Cq 常见问题 (FAQ)

这里收集了 Cq 使用中的常见问题及其解答。

## 安装与配置

### Q: 数据存储在哪里？

**A**: 默认情况下，知识库存储在：

- **macOS/Linux**: `~/.cq/knowledge.db`
- **Windows**: `%USERPROFILE%\.cq\knowledge.db`

你可以通过环境变量 `CQ_DB_PATH` 自定义路径：

```bash
export CQ_DB_PATH=/custom/path/knowledge.db
```

---

### Q: 如何在不同机器间迁移知识库？

**A**: 使用导出/导入功能：

```bash
# 在旧机器导出
cq-knowledge export --output cq-backup.json --feedback

# 在新机器安装
pip install cq-knowledge

# 在新机器导入
cq-knowledge import-cmd --input cq-backup.json
```

---

### Q: 支持哪些 Python 版本？

**A**: Cq 支持 Python 3.10 及以上版本：

- Python 3.10
- Python 3.11
- Python 3.12

检查你的 Python 版本：

```bash
python --version
```

---

### Q: 安装后命令不可用？

**A**: 尝试以下解决方案：

1. 确认安装成功：
```bash
pip show cq-knowledge
```

2. 检查 Python Scripts 目录在 PATH 中：
```bash
# Windows
echo %PATH%

# macOS/Linux
echo $PATH
```

3. 尝试使用 `python -m` 方式运行：
```bash
python -m cq.cli --help
```

---

## 搜索与使用

### Q: 搜索结果不准确怎么办？

**A**: 尝试以下方法：

1. **使用更具体的关键词**
   ```bash
   # 太宽泛
   cq-knowledge search "错误"

   # 更好
   cq-knowledge search "useEffect 无限循环"
   ```

2. **使用标签过滤**
   ```bash
   cq-knowledge search "循环" --tag python
   ```

3. **增加结果数量**
   ```bash
   cq-knowledge search "关键词" --limit 20
   ```

4. **检查知识单元内容**
   - 使用 `cq-knowledge show <ID>` 查看知识详情
   - 确认知识单元包含相关关键词

---

### Q: 如何批量导入知识？

**A**: 准备 JSON 文件后使用导入命令：

```bash
cq-knowledge import-cmd --input backup.json --skip-existing
```

JSON 格式示例：

```json
{
  "exported_at": "2024-03-26T00:00:00",
  "knowledge_units": [
    {
      "id": "unique-id-here",
      "title": "知识标题",
      "problem": "问题描述",
      "solution": "解决方案",
      "context": {"tags": ["tag1", "tag2"]},
      "confidence": 0.8
    }
  ]
}
```

---

### Q: 如何删除过时的知识？

**A**: 使用 delete 命令：

```bash
# 交互式删除（会确认）
cq-knowledge delete <知识ID>

# 强制删除
cq-knowledge delete <知识ID> --force
```

建议定期清理低置信度或长期未使用的知识。

---

## Claude Code / MCP 集成

### Q: Claude Code 中看不到 Cq 工具？

**A**: 按以下步骤排查：

1. **确认安装**
   ```bash
   pip show cq-knowledge
   ```

2. **检查配置文件**
   ```bash
   # macOS/Linux
   cat ~/.claude/config.json

   # Windows
   type %USERPROFILE%\.claude\config.json
   ```

   确保配置正确：
   ```json
   {
     "mcpServers": {
       "cq": {
         "command": "cq-knowledge-mcp"
       }
     }
   }
   ```

3. **完全重启 Claude Code**
   - 完全退出应用（不只是关闭窗口）
   - 重新打开

4. **查看日志**
   ```bash
   # macOS/Linux
   tail -f ~/.claude/logs/mcp.log

   # Windows
   type %USERPROFILE%\.claude\logs\mcp.log
   ```

---

### Q: MCP 工具调用报错？

**A**: 常见原因和解决方案：

1. **数据库未初始化**
   ```bash
   cq-knowledge init
   ```

2. **权限问题**
   - 检查 `~/.cq/` 目录权限
   - 确保当前用户有读写权限

3. **端口冲突**
   - 检查是否有其他进程占用

4. **依赖缺失**
   ```bash
   pip install --upgrade cq-knowledge
   ```

---

### Q: 可以在其他 IDE 中使用吗？

**A**: 是的！任何支持 MCP 协议的工具都可以集成 Cq：

- **Cline (Cursor)**: 配置方式与 Claude Code 类似
- **其他 MCP 客户端**: 配置命令为 `cq-knowledge-mcp`

参考 [MCP 集成指南](mcp-integration.md)。

---

## 置信度与反馈

### Q: 置信度评分是如何计算的？

**A**: 置信度基于用户反馈自动计算：

```
confidence = 0.5 + (正面 - 负面) / max(总数, 5) × 0.5
```

| 反馈情况 | 置信度 | 说明 |
|----------|--------|------|
| 无反馈 | 0.500 | 默认值 |
| 全部正面 (5/0) | 1.000 | 最高置信度 |
| 全部负面 (0/5) | 0.100 | 最低置信度 |
| 混合反馈 (3/2) | 0.600 | 按比例计算 |

至少需要 5 个反馈才能完全反映真实评分（减少早期波动）。

---

### Q: 如何手动调整置信度？

**A**: 使用反馈系统间接调整：

```bash
# 提升置信度（评分 4-5）
cq-knowledge feedback <ID> --rating 5

# 降低置信度（评分 1-3）
cq-knowledge feedback <ID> --rating 2
```

或使用重算命令：

```bash
# 预览变化
cq-knowledge recalculate --dry-run

# 应用变化
cq-knowledge recalculate
```

---

### Q: 评分规则是什么？

**A**:

| 评分 | 含义 | 对置信度影响 |
|------|------|--------------|
| 5 | 非常有帮助 | 大幅提升 |
| 4 | 有帮助 | 小幅提升 |
| 3 | 一般 | 无影响 |
| 2 | 没太大帮助 | 小幅降低 |
| 1 | 完全没帮助 | 大幅降低 |

---

## REST API

### Q: 如何在生产环境部署 API 服务？

**A**: 推荐使用反向代理（如 Nginx）：

```nginx
# Nginx 配置示例
location /api/ {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

使用进程管理器（如 systemd、supervisord）保持服务运行。

---

### Q: API 有速率限制吗？

**A**: 当前版本没有速率限制。建议在生产环境中通过反向代理添加：

```nginx
# Nginx 速率限制示例
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
location /api/ {
    limit_req zone=api burst=20;
    proxy_pass http://127.0.0.1:8000/;
}
```

---

### Q: 如何添加身份验证？

**A**: 当前版本不包含身份验证。建议：

1. **反向代理层添加认证**
   - Basic Auth
   - API Keys
   - OAuth2

2. **网络隔离**
   - 仅监听 localhost
   - 使用 VPN 或防火墙

---

## 数据安全与隐私

### Q: 数据会发送到云端吗？

**A**: **不会**。Cq 完全使用本地 SQLite 数据库，所有数据存储在本地，不会上传到任何服务器。

---

### Q: 如何加密知识库？

**A**: 可以使用文件系统级别的加密：

1. **加密整个目录** (推荐)
   ```bash
   # 使用 VeraCrypt 创建加密容器
   # 将 CQ_DB_PATH 指向加密容器内
   ```

2. **数据库加密**
   - 使用 SQLCipher 重新编译 aiosqlite
   - 需要修改源码

---

### Q: 如何备份知识库？

**A**:

```bash
# 方法1: 使用导出命令（推荐）
cq-knowledge export --output backup-$(date +%Y%m%d).json --feedback

# 方法2: 直接复制数据库文件
cp ~/.cq/knowledge.db ~/.cq/knowledge.db.backup

# 方法3: 定期自动备份（cron）
# 添加到 crontab:
0 2 * * * cq-knowledge export --output /backup/cq-$(date +\%Y\%m\%d).json
```

---

## 故障排除

### Q: 数据库损坏怎么办？

**A**:

1. **尝试恢复**
   ```bash
   # SQLite 恢复命令
   sqlite3 ~/.cq/knowledge.db ".recover" | sqlite3 recovered.db
   ```

2. **从备份恢复**
   ```bash
   cq-knowledge import-cmd --input backup.json
   ```

3. **重新初始化**（最后手段）
   ```bash
   rm ~/.cq/knowledge.db
   cq-knowledge init
   ```

---

### Q: 如何启用调试日志？

**A**:

```bash
# 设置环境变量
export CQ_LOG_LEVEL=DEBUG

# 然后运行命令
cq-knowledge search "test"
```

---

### Q: 如何完全卸载 Cq？

**A**:

```bash
# 卸载包
pip uninstall cq-knowledge

# 删除数据
rm -rf ~/.cq/

# 删除配置（如果有）
rm ~/.claude/config.json  # 或手动删除 cq 相关配置
```

---

## 其他

### Q: 支持中文搜索吗？

**A**: **是的**。SQLite FTS5 支持中文分词搜索：

```bash
cq-knowledge search "异步编程"
cq-knowledge search "useEffect 循环"
```

---

### Q: 如何贡献代码或报告问题？

**A**:

1. **报告 Bug**: 在 GitHub Issues 提交
2. **功能建议**: 在 GitHub Discussions 讨论
3. **贡献代码**: 参考 CONTRIBUTING.md 提交 Pull Request

---

### Q: 商业使用需要付费吗？

**A**: **不需要**。Cq 使用 Apache 2.0 许可证，可以免费用于商业用途。

---

## 仍未解决问题？

如果以上 FAQ 没有解答你的问题：

1. 查看 [完整文档](../README.md)
2. 在 GitHub 提交 [Issue](https://github.com/yourusername/cq/issues)
3. 加入社区讨论

---

## 相关文档

- [快速开始](getting-started.md)
- [CLI 命令参考](cli-reference.md)
- [MCP 集成指南](mcp-integration.md)
- [API 参考](api-reference.md)
