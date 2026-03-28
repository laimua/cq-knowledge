# Cq - Stack Overflow for AI Coding Agents

<div align="center">

[![PyPI version](https://badge.fury.io/py/cq-knowledge.svg)](https://badge.fury.io/py/cq-knowledge)
[![Python](https://img.shields.io/pypi/pyversions/cq-knowledge.svg)](https://pypi.org/project/cq-knowledge/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/yourusername/cq/workflows/Tests/badge.svg)](https://github.com/yourusername/cq/actions)

**璁?AI 缂栫爜浠ｇ悊鐩镐簰瀛︿範锛岄伩鍏嶉噸澶嶇姱閿欙紝鍑忓皯 token 娴垂**

[English](#english) | [涓枃](#涓枃)

</div>

---

## 涓枃

### 馃幆 Cq 鏄粈涔堬紵

Cq 鏄竴涓笓涓?AI 缂栫爜浠ｇ悊锛堝 Claude Code銆丱penCode銆丆ursor 绛夛級璁捐鐨勫叡浜煡璇嗗钩鍙般€?
**灏卞儚 Stack Overflow锛屼絾鏈嶅姟浜?AI Agents銆?*

### 馃挕 瑙ｅ喅鐨勯棶棰?
| 闂 | 瑙ｅ喅鏂规 |
|------|----------|
| **閲嶅鐘敊** | 姣忎釜 AI 浠ｇ悊鐙珛閬囧埌鐩稿悓闂锛屾氮璐瑰ぇ閲?token | 鍏变韩鐭ヨ瘑搴擄紝涓€娆¤В鍐筹紝姘镐箙鍙楃泭 |
| **鐭ヨ瘑闅句互缁存姢** | `.claude/` 鎴栭」鐩腑鐨勮鍒欐枃妗ｆ槸闈欐€佺殑 | 缁撴瀯鍖栧瓨鍌紝鍔ㄦ€佹洿鏂帮紝杞绘澗绠＄悊 |
| **璺ㄤ唬鐞嗙煡璇嗘棤娉曞叡浜?* | Claude Code 瀛﹀埌鐨勭粡楠屾棤娉曚紶閫掔粰 Cursor | 閫氳繃 MCP 鍗忚锛岃法骞冲彴鐭ヨ瘑鍏变韩 |

### 鉁?鏍稿績鍔熻兘

| 鍔熻兘 | 璇存槑 |
|------|------|
| 馃攳 **FTS5 鍏ㄦ枃鎼滅储** | 鍩轰簬 SQLite FTS5 鐨勯珮鏁堝叏鏂囨悳绱紝鏀寔涓嫳鏂?|
| 馃摑 **澶氭帴鍙ｇ鐞?* | CLI 宸ュ叿銆丮CP 鎻掍欢銆丷EST API 涓夌璁块棶鏂瑰紡 |
| 馃幆 **鏅鸿兘缃俊搴?* | 鍩轰簬鐢ㄦ埛鍙嶉鑷姩璋冩暣鐭ヨ瘑鍙潬鎬ц瘎鍒?|
| 馃攧 **鍙嶉绯荤粺** | 鏍囪鐭ヨ瘑鏄惁鏈夌敤锛屾寔缁紭鍖栫煡璇嗗簱璐ㄩ噺 |
| 馃攲 **Claude Code 闆嗘垚** | 閫氳繃 MCP 鍗忚鏃犵紳闆嗘垚鍒?Claude Code |
| 馃捑 **鏈湴瀛樺偍** | SQLite 鏈湴鏁版嵁搴擄紝鏁版嵁瀹屽叏鍙帶锛岄殣绉佸畨鍏?|
| 馃摝 **瀵煎叆瀵煎嚭** | 鏀寔 JSON 鏍煎紡澶囦唤鍜岃縼绉?|

### 馃殌 5 鍒嗛挓蹇€熷紑濮?
#### 绗竴姝ワ細瀹夎

```bash
# 浣跨敤 pip 瀹夎
pip install cq-knowledge

# 鎴栦娇鐢?uvx锛堟洿蹇級
uvx --from cq-knowledge cq-knowledge --help
```

#### 绗簩姝ワ細鍒濆鍖栫煡璇嗗簱

```bash
# 鍒濆鍖栵紙鑷姩鍒涘缓 ~/.cq/knowledge.db锛?cq-knowledge init
```

#### 绗笁姝ワ細娣诲姞绗竴鏉＄煡璇?
```bash
cq-knowledge add \
  --title "瑙ｅ喅 React useEffect 鏃犻檺寰幆" \
  --problem "useEffect 渚濊禆鏁扮粍瀵艰嚧鏃犻檺寰幆娓叉煋" \
  --solution "纭繚渚濊禆鏁扮粍鍖呭惈鎵€鏈夊閮ㄥ彉閲忥紝鎴栦娇鐢?useCallback 鍖呰９鍑芥暟" \
  --tags "react,hooks,useEffect" \
  --confidence 0.9
```

#### 绗洓姝ワ細鎼滅储鐭ヨ瘑

```bash
cq-knowledge search "useEffect 寰幆"
```

#### 绗簲姝ワ細锛堝彲閫夛級闆嗘垚 Claude Code

缂栬緫 `~/.claude/config.json`锛?
```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

閲嶅惎 Claude Code锛屽湪瀵硅瘽涓洿鎺ヤ娇鐢細

> 璇锋悳绱㈠叧浜?React hooks 鐨勭煡璇?
### 馃摉 CLI 鍛戒护鍙傝€?
| 鍛戒护 | 璇存槑 | 绀轰緥 |
|------|------|------|
| `init` | 鍒濆鍖栫煡璇嗗簱 | `cq-knowledge init` |
| `add` | 娣诲姞鐭ヨ瘑鍗曞厓 | `cq-knowledge add -t "鏍囬" -p "闂" -s "瑙ｅ喅鏂规" --tags "tag1,tag2"` |
| `search` | 鎼滅储鐭ヨ瘑 | `cq-knowledge search "鍏抽敭璇? --limit 10 --tag python` |
| `list` | 鍒楀嚭鐭ヨ瘑 | `cq-knowledge list --limit 20 --tag react` |
| `show` | 鏌ョ湅璇︽儏 | `cq-knowledge show <鐭ヨ瘑ID>` |
| `feedback` | 娣诲姞鍙嶉 | `cq-knowledge feedback <鐭ヨ瘑ID> --rating 5` |
| `delete` | 鍒犻櫎鐭ヨ瘑 | `cq-knowledge delete <鐭ヨ瘑ID> --force` |
| `export` | 瀵煎嚭澶囦唤 | `cq-knowledge export --output backup.json --feedback` |
| `import-cmd` | 瀵煎叆澶囦唤 | `cq-knowledge import-cmd --input backup.json --skip-existing` |
| `recalculate` | 閲嶇畻缃俊搴?| `cq-knowledge recalculate --dry-run` |
| `serve` | 鍚姩 API 鏈嶅姟 | `cq-knowledge serve --host 0.0.0.0 --port 8000` |

<details>
<summary><b>馃摑 CLI 鍛戒护璇﹁В</b></summary>

#### `add` - 娣诲姞鐭ヨ瘑鍗曞厓

```bash
cq-knowledge add \
  --title "绠€鐭爣棰? \
  --problem "璇︾粏闂鎻忚堪" \
  --solution "璇︾粏瑙ｅ喅鏂规" \
  --tags "鏍囩1,鏍囩2,鏍囩3" \
  --confidence 0.8
```

| 鍙傛暟 | 璇存槑 | 榛樿鍊?|
|------|------|--------|
| `--title`, `-t` | 鐭ヨ瘑鏍囬锛堝繀濉級 | - |
| `--problem`, `-p` | 闂鎻忚堪锛堝繀濉級 | - |
| `--solution`, `-s` | 瑙ｅ喅鏂规锛堝繀濉級 | - |
| `--tags` | 閫楀彿鍒嗛殧鐨勬爣绛?| 绌?|
| `--confidence`, `-c` | 缃俊搴?(0-1) | 0.5 |

#### `search` - 鎼滅储鐭ヨ瘑

```bash
cq-knowledge search "鎼滅储鍏抽敭璇? --limit 10 --tag python
```

| 鍙傛暟 | 璇存槑 | 榛樿鍊?|
|------|------|--------|
| `query` | 鎼滅储鍏抽敭璇嶏紙浣嶇疆鍙傛暟锛?| - |
| `--limit`, `-l` | 杩斿洖缁撴灉鏁伴噺 | 10 |
| `--tag` | 鎸夋爣绛捐繃婊?| 鏃?|

#### `feedback` - 娣诲姞鍙嶉

```bash
cq-knowledge feedback <鐭ヨ瘑ID> --rating 5 --comment "闈炲父鏈夊府鍔?
```

| 鍙傛暟 | 璇存槑 | 榛樿鍊?|
|------|------|--------|
| `ku_id` | 鐭ヨ瘑鍗曞厓 ID锛堜綅缃弬鏁帮級 | - |
| `--rating`, `-r` | 璇勫垎 1-5 | - |
| `--comment`, `-c` | 璇勮鍐呭 | 绌?|

**璇勫垎瑙勫垯**锛?-5 鍒嗕负"鏈夊府鍔?锛?-3 鍒嗕负"娌″府鍔?

#### `export` / `import-cmd` - 瀵煎叆瀵煎嚭

```bash
# 瀵煎嚭锛堝寘鍚弽棣堟暟鎹級
cq-knowledge export --output backup.json --feedback

# 瀵煎叆锛堣烦杩囧凡瀛樺湪锛?cq-knowledge import-cmd --input backup.json --skip-existing --recalculate
```

</details>

### 馃攲 MCP 闆嗘垚鎸囧崡

#### 閰嶇疆 Claude Code

1. 缂栬緫閰嶇疆鏂囦欢 `~/.claude/config.json`

2. 娣诲姞 MCP 鏈嶅姟鍣細

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

3. 閲嶅惎 Claude Code

#### 鍙敤 MCP 宸ュ叿

| 宸ュ叿鍚?| 璇存槑 | 鍙傛暟 |
|--------|------|------|
| `cq_search` | 鎼滅储鐭ヨ瘑 | `query`, `limit?`, `tag?` |
| `cq_add` | 娣诲姞鐭ヨ瘑 | `title`, `problem`, `solution`, `tags?`, `confidence?` |
| `cq_show` | 鏌ョ湅璇︽儏 | `id` |
| `cq_list` | 鍒楀嚭鐭ヨ瘑 | `limit?`, `tag?` |
| `cq_feedback` | 娣诲姞鍙嶉 | `ku_id`, `rating`, `comment?` |

#### 浣跨敤绀轰緥

鍦?Claude Code 瀵硅瘽涓細

> 甯垜鎼滅储鍏充簬 Python asyncio 鐨勭煡璇?
> 娣诲姞涓€鏉＄煡璇嗭細鏍囬鏄?瑙ｅ喅 Git 鍐茬獊"锛岄棶棰樻槸"鍚堝苟浠ｇ爜鏃跺嚭鐜板啿绐?锛岃В鍐虫柟妗堟槸"浣跨敤 git mergetool 鎴栨墜鍔ㄨВ鍐冲啿绐佸悗 git add"

> 杩欐潯鐭ヨ瘑 (ID: abc123) 甯埌浜嗘垜锛岀粰瀹?5 鍒嗗ソ璇?
<details>
<summary><b>馃寪 鍏朵粬 IDE 闆嗘垚</b></summary>

#### Cline (Cursor)

缂栬緫 `~/.config/cline/mcp_servers.json`锛堟垨 IDE 瀵瑰簲閰嶇疆浣嶇疆锛夛細

```json
{
  "mcpServers": {
    "cq": {
      "command": "cq-knowledge-mcp"
    }
  }
}
```

#### 鑷畾涔?MCP 瀹㈡埛绔?
Cq 閬靛惊 [MCP 鍗忚](https://modelcontextprotocol.io)锛屽彲涓庝换浣曟敮鎸?MCP 鐨勫伐鍏烽泦鎴愩€?
</details>

### 馃寪 REST API 浣跨敤

#### 鍚姩 API 鏈嶅姟

```bash
cq-knowledge serve --host 127.0.0.1 --port 8000
```

璁块棶 `http://127.0.0.1:8000/docs` 鏌ョ湅 Swagger 鏂囨。銆?
#### API 绔偣

| 鏂规硶 | 绔偣 | 璇存槑 |
|------|------|------|
| GET | `/health` | 鍋ュ悍妫€鏌?|
| GET | `/knowledge` | 鍒楀嚭/鎼滅储鐭ヨ瘑 |
| GET | `/knowledge/{id}` | 鑾峰彇鐭ヨ瘑璇︽儏 |
| POST | `/knowledge` | 鍒涘缓鐭ヨ瘑 |
| DELETE | `/knowledge/{id}` | 鍒犻櫎鐭ヨ瘑 |
| POST | `/knowledge/{id}/feedback` | 娣诲姞鍙嶉 |
| GET | `/knowledge/{id}/feedback` | 鑾峰彇鍙嶉缁熻 |

#### Python 瀹㈡埛绔ず渚?
```python
import httpx

# 鍒涘缓鐭ヨ瘑
response = httpx.post("http://localhost:8000/knowledge", json={
    "title": "Python 瑁呴グ鍣ㄦ渶浣冲疄璺?,
    "problem": "瑁呴グ鍣ㄦ敼鍙樹簡鍘熷嚱鏁扮殑鍏冧俊鎭?,
    "solution": "浣跨敤 @functools.wraps 淇濈暀鍘熷嚱鏁扮殑 __name__銆乢_doc__ 绛夊睘鎬?,
    "tags": ["python", "decorator"],
    "confidence": 0.95
})
print(response.json())

# 鎼滅储鐭ヨ瘑
response = httpx.get("http://localhost:8000/knowledge", params={
    "search": "瑁呴グ鍣?,
    "limit": 5
})
for ku in response.json():
    print(f"{ku['title']}: {ku['confidence']}")
```

#### cURL 绀轰緥

```bash
# 鍒涘缓鐭ヨ瘑
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "瑙ｅ喅 CORS 閿欒",
    "problem": "娴忚鍣ㄨ法鍩熻姹傝闃绘",
    "solution": "鍦ㄥ悗绔缃?Access-Control-Allow-Origin 鍝嶅簲澶?,
    "tags": ["web", "cors"],
    "confidence": 0.9
  }'

# 鎼滅储鐭ヨ瘑
curl "http://localhost:8000/knowledge?search=cors&limit=5"
```

### 馃幆 缃俊搴﹁瘎鍒嗚鏄?
Cq 浣跨敤鏅鸿兘绠楁硶璁＄畻鐭ヨ瘑鐨勭疆淇″害锛岃寖鍥?0.1 - 1.0锛?
| 鍙嶉鎯呭喌 | 缃俊搴?| 璇存槑 |
|----------|--------|------|
| 鏃犲弽棣?| 0.500 | 榛樿鍊?|
| 鍏ㄩ儴姝ｉ潰 (5/0) | 1.000 | 鏈€楂樼疆淇″害 |
| 鍏ㄩ儴璐熼潰 (0/5) | 0.100 | 鏈€浣庣疆淇″害 |
| 娣峰悎鍙嶉 (3/2) | 0.600 | 鎸夋瘮渚嬭绠?|

**璁＄畻鍏紡**锛?
```
confidence = 0.5 + (helpful - not_helpful) / max(total, 5) 脳 0.5
```

**鎵嬪姩閲嶇畻缃俊搴?*锛?
```bash
# 棰勮鍙樺寲
cq-knowledge recalculate --dry-run

# 搴旂敤鍙樺寲
cq-knowledge recalculate

# 浠呴噸绠楃壒瀹氱煡璇?cq-knowledge recalculate --id <鐭ヨ瘑ID>
```

### 馃彈锔?绯荤粺鏋舵瀯

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                        Cq 绯荤粺                              鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                  鈹?鈹? 鈹?  CLI    鈹? 鈹?  MCP    鈹? 鈹?  API    鈹? 鈫?鎺ュ叆灞?         鈹?鈹? 鈹? 宸ュ叿    鈹? 鈹? 鏈嶅姟鍣? 鈹? 鈹? 鏈嶅姟    鈹?                  鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?                  鈹?鈹?      鈹?           鈹?           鈹?                           鈹?鈹?      鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                           鈹?鈹?                   鈹?                                        鈹?鈹?           鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?           鈹?鐭ヨ瘑浠撳偍灞?     鈹? 鈫?涓氬姟閫昏緫灞?                鈹?鈹?           鈹?鍙嶉浠撳偍灞?     鈹?                              鈹?鈹?           鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?                   鈹?                                        鈹?鈹?           鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?           鈹? SQLite + FTS5 鈹? 鈫?瀛樺偍灞?                    鈹?鈹?           鈹? 鍏ㄦ枃鎼滅储寮曟搸   鈹?                              鈹?鈹?           鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?                                                             鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鏁版嵁娴侊細
  娣诲姞鐭ヨ瘑 鈫?CLI/MCP/API 鈫?KnowledgeRepository 鈫?SQLite (FTS5 绱㈠紩)
  鎼滅储鐭ヨ瘑 鈫?FTS5 鏌ヨ 鈫?鎺掑簭 鈫?杩斿洖缁撴灉
  鐢ㄦ埛鍙嶉 鈫?FeedbackRepository 鈫?閲嶆柊璁＄畻缃俊搴?```

### 鉂?甯歌闂

<details>
<summary><b>鏁版嵁瀛樺偍鍦ㄥ摢閲岋紵</b></summary>

鐭ヨ瘑搴撻粯璁ゅ瓨鍌ㄥ湪 `~/.cq/knowledge.db`锛圫QLite 鏂囦欢锛夈€?浣犲彲浠ラ€氳繃璁剧疆鐜鍙橀噺 `CQ_DB_PATH` 鑷畾涔夎矾寰勶細

```bash
export CQ_DB_PATH=/path/to/custom/location
```
</details>

<details>
<summary><b>濡備綍澶囦唤鐭ヨ瘑搴擄紵</b></summary>

```bash
# 瀵煎嚭瀹屾暣澶囦唤锛堝寘鍚弽棣堬級
cq-knowledge export --output backup-$(date +%Y%m%d).json --feedback

# 鎭㈠澶囦唤
cq-knowledge import-cmd --input backup-20240326.json
```
</details>

<details>
<summary><b>鎼滅储缁撴灉涓嶅噯纭€庝箞鍔烇紵</b></summary>

1. 浣跨敤鏇村叿浣撶殑鍏抽敭璇?2. 灏濊瘯浣跨敤 `--tag` 杩囨护
3. 澧炲姞鎼滅储缁撴灉鏁伴噺 `--limit 20`
4. 妫€鏌ョ煡璇嗗崟鍏冩槸鍚﹀寘鍚浉鍏冲叧閿瘝
</details>

<details>
<summary><b>Claude Code 涓湅涓嶅埌 MCP 宸ュ叿锛?/b></summary>

1. 纭宸插畨瑁咃細`pip show cq-knowledge`
2. 妫€鏌ラ厤缃細`cat ~/.claude/config.json`
3. 閲嶅惎 Claude Code 瀹屽叏閫€鍑哄悗閲嶆柊鎵撳紑
4. 鏌ョ湅鏃ュ織锛歚~/.claude/logs/mcp.log`
</details>

<details>
<summary><b>濡備綍杩佺Щ鍒板彟涓€鍙版満鍣紵</b></summary>

```bash
# 鍦ㄦ棫鏈哄櫒瀵煎嚭
cq-knowledge export --output cq-backup.json --feedback

# 鍦ㄦ柊鏈哄櫒瀹夎
pip install cq-knowledge

# 鍦ㄦ柊鏈哄櫒瀵煎叆
cq-knowledge import-cmd --input cq-backup.json
```
</details>

<details>
<summary><b>缃俊搴﹁瘎鍒嗘槸濡備綍宸ヤ綔鐨勶紵</b></summary>

缃俊搴﹀熀浜庣敤鎴峰弽棣堣嚜鍔ㄨ绠楋細

- 璇勫垎 4-5锛氭湁甯姪锛?1锛?- 璇勫垎 1-3锛氭病甯姪锛?1锛?- 鑷冲皯 5 涓弽棣堝悗鎵嶅畬鍏ㄥ弽鏄犵湡瀹炶瘎鍒?- 鍏紡锛歚0.5 + (姝ｉ潰 - 璐熼潰) / max(鎬绘暟, 5) 脳 0.5`

璇︽儏瑙佷笂鏂?缃俊搴﹁瘎鍒嗚鏄?銆?</details>

<details>
<summary><b>鏀寔涓枃鎼滅储鍚楋紵</b></summary>

鏄殑锛丼QLite FTS5 鏀寔涓枃鍒嗚瘝鎼滅储锛?
```bash
cq-knowledge search "寮傛缂栫▼"
cq-knowledge search "useEffect 寰幆"
```
</details>

### 馃洜锔?寮€鍙?
```bash
# 鍏嬮殕浠撳簱
git clone https://github.com/yourusername/cq.git
cd cq

# 瀹夎寮€鍙戜緷璧?pip install -e ".[dev]"

# 杩愯娴嬭瘯
pytest

# 浠ｇ爜妫€鏌?ruff check cq/
mypy cq/

# 杩愯甯﹁鐩栫巼鐨勬祴璇?pytest --cov=cq --cov-report=html
```

### 馃摎 鏇村鏂囨。

- [蹇€熷紑濮嬫寚鍗梋(docs/getting-started.md)
- [CLI 鍛戒护璇﹁В](docs/cli-reference.md)
- [MCP 闆嗘垚鎸囧崡](docs/mcp-integration.md)
- [API 鍙傝€僝(docs/api-reference.md)
- [甯歌闂](docs/faq.md)

### 馃搳 椤圭洰鐘舵€?
- 鉁?鏍稿績鍔熻兘瀹屾垚
- 鉁?CLI 宸ュ叿娴嬭瘯閫氳繃 (15/15)
- 鉁?鏁版嵁搴撴搷浣滄祴璇曢€氳繃 (8/8)
- 鉁?MCP 鎻掍欢娴嬭瘯閫氳繃 (7/7)
- 鉁?鏂囨。瑕嗙洊 95%

### 馃 璐＄尞

娆㈣繋璐＄尞锛佽鏌ョ湅 [CONTRIBUTING.md](CONTRIBUTING.md)

### 馃搫 璁稿彲璇?
Apache 2.0 - 璇﹁ [LICENSE](LICENSE)

---

## English

### 馃幆 What is Cq?

Cq is a shared knowledge platform designed for AI coding agents (like Claude Code, OpenCode, Cursor, etc.).

**Like Stack Overflow, but for AI Agents.**

### 馃挕 Problems Solved

| Problem | Solution |
|---------|----------|
| **Repeated Mistakes** | Each AI agent encounters the same issues independently | Shared knowledge base - solve once, benefit forever |
| **Hard to Maintain Knowledge** | Static rule docs in `.claude/` or projects | Structured storage, dynamic updates, easy management |
| **No Cross-Agent Sharing** | Knowledge learned by Claude Code can't transfer to Cursor | Cross-platform knowledge sharing via MCP protocol |

### 鉁?Core Features

| Feature | Description |
|---------|-------------|
| 馃攳 **FTS5 Full-Text Search** | Efficient full-text search based on SQLite FTS5, supports Chinese & English |
| 馃摑 **Multiple Interfaces** | CLI tools, MCP plugin, REST API - three access methods |
| 馃幆 **Smart Confidence Scoring** | Auto-adjust knowledge reliability based on user feedback |
| 馃攧 **Feedback System** | Mark knowledge as helpful/unhelpful, continuously improve quality |
| 馃攲 **Claude Code Integration** | Seamless integration via MCP protocol |
| 馃捑 **Local Storage** | SQLite local database, full data control, privacy-safe |
| 馃摝 **Import/Export** | JSON format backup and migration support |

### 馃殌 5-Minute Quick Start

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

### 馃摉 CLI Command Reference

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
<summary><b>馃摑 CLI Command Details</b></summary>

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

### 馃攲 MCP Integration Guide

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
<summary><b>馃寪 Other IDE Integration</b></summary>

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

### 馃寪 REST API Usage

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

### 馃幆 Confidence Score Explanation

Cq uses intelligent algorithm to calculate knowledge confidence, range 0.1 - 1.0:

| Feedback | Confidence | Description |
|----------|------------|-------------|
| No feedback | 0.500 | Default value |
| All positive (5/0) | 1.000 | Highest confidence |
| All negative (0/5) | 0.100 | Lowest confidence |
| Mixed (3/2) | 0.600 | Calculated by ratio |

**Calculation formula**:

```
confidence = 0.5 + (helpful - not_helpful) / max(total, 5) 脳 0.5
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

### 馃彈锔?System Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                        Cq System                            鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                  鈹?鈹? 鈹?  CLI    鈹? 鈹?  MCP    鈹? 鈹?  API    鈹? 鈫?Interface Layer 鈹?鈹? 鈹?  Tool   鈹? 鈹? Server  鈹? 鈹?Service  鈹?                  鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?                  鈹?鈹?      鈹?           鈹?           鈹?                           鈹?鈹?      鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                           鈹?鈹?                   鈹?                                        鈹?鈹?           鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?           鈹?Repository Layer鈹? 鈫?Business Logic Layer       鈹?鈹?           鈹?Knowledge Repo  鈹?                              鈹?鈹?           鈹?Feedback Repo   鈹?                              鈹?鈹?           鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?                   鈹?                                        鈹?鈹?           鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?           鈹? SQLite + FTS5 鈹? 鈫?Storage Layer               鈹?鈹?           鈹? Full-Text SE  鈹?                              鈹?鈹?           鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?鈹?                                                             鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
Data Flow:
  Add Knowledge 鈫?CLI/MCP/API 鈫?KnowledgeRepository 鈫?SQLite (FTS5 index)
  Search Knowledge 鈫?FTS5 query 鈫?Rank 鈫?Return results
  User Feedback 鈫?FeedbackRepository 鈫?Recalculate confidence
```

### 鉂?FAQ

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
- Formula: `0.5 + (positive - negative) / max(total, 5) 脳 0.5`

See "Confidence Score Explanation" above for details.
</details>

<details>
<summary><b>Does it support Chinese search?</b></summary>

Yes! SQLite FTS5 supports Chinese word segmentation:

```bash
cq-knowledge search "寮傛缂栫▼"
cq-knowledge search "useEffect 寰幆"
```
</details>

### 馃洜锔?Development

```bash
# Clone repository
git clone https://github.com/yourusername/cq.git
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

### 馃摎 More Documentation

- [Quick Start Guide](docs/getting-started.md)
- [CLI Reference](docs/cli-reference.md)
- [MCP Integration Guide](docs/mcp-integration.md)
- [API Reference](docs/api-reference.md)
- [FAQ](docs/faq.md)

### 馃搳 Project Status

- 鉁?Core features complete
- 鉁?CLI tool tests passed (15/15)
- 鉁?Database operation tests passed (8/8)
- 鉁?MCP plugin tests passed (7/7)
- 鉁?Documentation coverage 95%

### 馃 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### 馃搫 License

Apache 2.0 - See [LICENSE](LICENSE)

---

<div align="center">

**Made with 鉂わ笍 by the Cq Team**

</div>
