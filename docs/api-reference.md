# Cq REST API 参考

Cq 提供 RESTful API 用于程序化访问知识库。

## 启动 API 服务

```bash
# 默认配置 (127.0.0.1:8000)
cq-knowledge serve

# 自定义配置
cq-knowledge serve --host 0.0.0.0 --port 8080

# 开发模式（自动重载）
cq-knowledge serve --reload
```

启动后访问：
- **API 文档**: http://127.0.0.1:8000/docs (Swagger UI)
- **备选文档**: http://127.0.0.1:8000/redoc (ReDoc)

## API 概览

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/knowledge` | 列出/搜索知识 |
| GET | `/knowledge/{id}` | 获取知识详情 |
| POST | `/knowledge` | 创建知识 |
| DELETE | `/knowledge/{id}` | 删除知识 |
| POST | `/knowledge/{id}/feedback` | 添加反馈 |
| GET | `/knowledge/{id}/feedback` | 获取反馈统计 |

## 数据模型

### KnowledgeCreateRequest

创建知识单元的请求。

| 字段 | 类型 | 必填 | 说明 | 约束 |
|------|------|------|------|------|
| `title` | string | ✅ | 知识标题 | 最大 200 字符 |
| `problem` | string | ✅ | 问题描述 | 最大 2000 字符 |
| `solution` | string | ✅ | 解决方案 | 最大 5000 字符 |
| `tags` | string[] | ❌ | 标签列表 | 默认 `[]` |
| `confidence` | float | ❌ | 置信度 | 0-1，默认 0.5 |
| `source` | string | ❌ | 来源 | 默认 "manual" |

### KnowledgeResponse

知识单元的响应。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 知识单元 ID |
| `title` | string | 标题 |
| `problem` | string | 问题描述 |
| `solution` | string | 解决方案 |
| `context` | object | 上下文数据 |
| `confidence` | float | 置信度 (0-1) |
| `usage_count` | int | 使用次数 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |
| `source` | string | 来源 |
| `verified` | boolean | 是否验证 |
| `tags` | string[] | 标签列表 |

### FeedbackRequest

提交反馈的请求。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `helpful` | boolean | ✅ | 是否有帮助 |
| `source` | string | ❌ | 评论或来源 |

### FeedbackStatsResponse

反馈统计的响应。

| 字段 | 类型 | 说明 |
|------|------|------|
| `helpful_count` | int | 有帮助数量 |
| `not_helpful_count` | int | 没帮助数量 |
| `total_count` | int | 总数量 |

## 端点详解

### GET /health

健康检查端点。

**请求**：

```http
GET /health
```

**响应**：

```json
{
  "status": "healthy",
  "service": "cq-knowledge-api"
}
```

**状态码**：
- `200 OK`: 服务正常

---

### GET /knowledge

列出或搜索知识单元。

**请求参数**：

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `search` | string | ❌ | 搜索关键词（启用 FTS5） | - |
| `tags` | string | ❌ | 逗号分隔的标签过滤 | - |
| `limit` | int | ❌ | 返回结果数量 | 20 |
| `offset` | int | ❌ | 跳过前 N 条 | 0 |

**请求示例**：

```http
GET /knowledge?search=useEffect&limit=10
GET /knowledge?tags=python,asyncio
GET /knowledge?search=循环&tags=python&limit=5
GET /knowledge?limit=20&offset=20
```

**响应**：

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "React useEffect 无限循环",
    "problem": "useEffect 依赖数组导致无限循环渲染",
    "solution": "确保依赖数组包含所有外部变量",
    "context": { "tags": ["react", "hooks"] },
    "confidence": 0.9,
    "usage_count": 5,
    "created_at": "2024-03-26T10:30:00",
    "updated_at": "2024-03-26T15:45:00",
    "source": "manual",
    "verified": false,
    "tags": ["react", "hooks"]
  }
]
```

**状态码**：
- `200 OK`: 成功

---

### GET /knowledge/{id}

获取知识单元详情。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 知识单元 ID |

**请求示例**：

```http
GET /knowledge/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**响应**：

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "React useEffect 无限循环",
  "problem": "useEffect 依赖数组导致无限循环渲染",
  "solution": "确保依赖数组包含所有外部变量，或使用 useCallback 包裹函数",
  "context": { "tags": ["react", "hooks", "useEffect"] },
  "confidence": 0.9,
  "usage_count": 5,
  "created_at": "2024-03-26T10:30:00",
  "updated_at": "2024-03-26T15:45:00",
  "source": "manual",
  "verified": false,
  "tags": ["react", "hooks", "useEffect"]
}
```

**状态码**：
- `200 OK`: 成功
- `404 Not Found`: 知识单元不存在

---

### POST /knowledge

创建新的知识单元。

**请求体**：

```json
{
  "title": "解决 CORS 错误",
  "problem": "浏览器跨域请求被阻止",
  "solution": "在后端设置 Access-Control-Allow-Origin 响应头",
  "tags": ["web", "cors", "javascript"],
  "confidence": 0.9,
  "source": "api"
}
```

**响应**：

```json
{
  "id": "b2c3d4e5-f6g7-8901-bcde-f12345678901",
  "title": "解决 CORS 错误",
  "problem": "浏览器跨域请求被阻止",
  "solution": "在后端设置 Access-Control-Allow-Origin 响应头",
  "context": { "tags": ["web", "cors", "javascript"] },
  "confidence": 0.9,
  "usage_count": 0,
  "created_at": "2024-03-26T16:00:00",
  "updated_at": "2024-03-26T16:00:00",
  "source": "api",
  "verified": false,
  "tags": ["web", "cors", "javascript"]
}
```

**状态码**：
- `201 Created`: 创建成功

---

### DELETE /knowledge/{id}

删除知识单元。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 知识单元 ID |

**请求示例**：

```http
DELETE /knowledge/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**响应**：

无内容（状态码 204）

**状态码**：
- `204 No Content`: 删除成功
- `404 Not Found`: 知识单元不存在

---

### POST /knowledge/{id}/feedback

为知识单元添加反馈。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 知识单元 ID |

**请求体**：

```json
{
  "helpful": true,
  "source": "通过 API 解决了我的问题"
}
```

**响应**：

```json
{
  "helpful_count": 5,
  "not_helpful_count": 1,
  "total_count": 6
}
```

**状态码**：
- `200 OK`: 反馈成功
- `404 Not Found`: 知识单元不存在

---

### GET /knowledge/{id}/feedback

获取知识单元的反馈统计。

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 知识单元 ID |

**请求示例**：

```http
GET /knowledge/a1b2c3d4-e5f6-7890-abcd-ef1234567890/feedback
```

**响应**：

```json
{
  "helpful_count": 5,
  "not_helpful_count": 1,
  "total_count": 6
}
```

**状态码**：
- `200 OK`: 成功

---

## 使用示例

### Python (httpx)

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
ku = response.json()
print(f"Created: {ku['id']}")

# 搜索知识
response = httpx.get("http://localhost:8000/knowledge", params={
    "search": "装饰器",
    "limit": 5
})
for ku in response.json():
    print(f"{ku['title']}: {ku['confidence']}")

# 添加反馈
response = httpx.post(
    f"http://localhost:8000/knowledge/{ku['id']}/feedback",
    json={"helpful": True, "source": "很有帮助"}
)
print(response.json())

# 删除知识
response = httpx.delete(f"http://localhost:8000/knowledge/{ku['id']}")
print(f"Deleted: {response.status_code == 204}")
```

### JavaScript (fetch)

```javascript
// 创建知识
const response = await fetch('http://localhost:8000/knowledge', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: '解决 CORS 错误',
    problem: '浏览器跨域请求被阻止',
    solution: '在后端设置 Access-Control-Allow-Origin 响应头',
    tags: ['web', 'cors'],
    confidence: 0.9
  })
});
const ku = await response.json();
console.log('Created:', ku.id);

// 搜索知识
const response = await fetch(
  'http://localhost:8000/knowledge?search=cors&limit=5'
);
const results = await response.json();
results.forEach(ku => console.log(`${ku.title}: ${ku.confidence}`));

// 添加反馈
await fetch(`http://localhost:8000/knowledge/${ku.id}/feedback`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    helpful: true,
    source: '很有帮助'
  })
});
```

### cURL

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

# 获取详情
curl http://localhost:8000/knowledge/{id}

# 添加反馈
curl -X POST http://localhost:8000/knowledge/{id}/feedback \
  -H "Content-Type: application/json" \
  -d '{"helpful": true, "source": "很有帮助"}'

# 删除知识
curl -X DELETE http://localhost:8000/knowledge/{id}
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
)

func main() {
    // 创建知识
    ku := map[string]interface{}{
        "title":      "解决 CORS 错误",
        "problem":    "浏览器跨域请求被阻止",
        "solution":   "在后端设置 Access-Control-Allow-Origin 响应头",
        "tags":       []string{"web", "cors"},
        "confidence": 0.9,
    }
    body, _ := json.Marshal(ku)

    resp, _ := http.Post(
        "http://localhost:8000/knowledge",
        "application/json",
        bytes.NewBuffer(body),
    )
    defer resp.Close()

    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    println("Created:", result["id"].(string))
}
```

## 错误响应

所有错误端点返回统一格式：

```json
{
  "detail": "错误描述信息"
}
```

常见 HTTP 状态码：

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无内容） |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 验证错误 |
| 500 | 服务器内部错误 |

## 速率限制

当前版本没有速率限制，建议在生产环境中通过反向代理（如 Nginx）添加。

## CORS

API 默认允许所有来源的跨域请求。如需限制，请使用反向代理配置。

## 相关文档

- [快速开始](getting-started.md)
- [CLI 命令参考](cli-reference.md)
- [MCP 集成指南](mcp-integration.md)
- [常见问题](faq.md)
