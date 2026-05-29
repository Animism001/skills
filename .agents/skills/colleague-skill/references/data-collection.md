# 数据采集指南

## 方式 A：飞书自动采集（推荐）

首次使用需配置：
```bash
python3 tools/feishu_auto_collector.py --setup
```

### 群聊采集（tenant_access_token，需 bot 在群内）

```bash
python3 tools/feishu_auto_collector.py \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 1000 \
  --doc-limit 20
```

### 私聊采集（user_access_token + chat_id）

私聊消息只能通过用户身份获取，应用身份无权访问。

**前置条件**：
1. 飞书应用凭证：`app_id` + `app_secret`
2. 用户权限：`im:message` + `im:chat`
3. OAuth 授权码

**获取 user_access_token**：
1. 生成 OAuth 链接：
   ```
   https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={APP_ID}&redirect_uri=http://www.example.com&scope=im:message%20im:chat
   ```
2. 用户授权后，从回调 URL 获取 code
3. 换取 token：
   ```bash
   python3 tools/feishu_auto_collector.py --exchange-code {CODE}
   ```

**获取私聊 chat_id**：
- 向对方 open_id 发消息，返回值中包含 chat_id
- `GET /im/v1/chats` 不返回私聊会话（飞书 API 限制）

**执行采集**：
```bash
python3 tools/feishu_auto_collector.py \
  --open-id {对方open_id} \
  --p2p-chat-id {chat_id} \
  --user-token {user_access_token} \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 1000
```

**灵活性原则**：脚本跑不通时可直接写 Python 调飞书 API。

**采集输出**：
- `knowledge/{slug}/messages.txt`
- `knowledge/{slug}/docs.txt`
- `knowledge/{slug}/collection_summary.json`

## 方式 B：钉钉自动采集

```bash
python3 tools/dingtalk_auto_collector.py --setup  # 首次配置
python3 tools/dingtalk_auto_collector.py \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 500 \
  --doc-limit 20 \
  --show-browser   # 首次使用
```

钉钉 API 不支持历史消息拉取，自动切换浏览器采集。

## 方式 C：飞书链接

选择读取方式：
1. **浏览器方案**（推荐）— 复用 Chrome 登录态，无需配置
   ```bash
   python3 tools/feishu_browser.py --url "{url}" --target "{name}" --output /tmp/feishu_doc_out.txt
   ```
2. **MCP 方案** — 稳定，需配置 App ID/Secret
   ```bash
   python3 tools/feishu_mcp_client.py --setup  # 首次配置
   python3 tools/feishu_mcp_client.py --url "{url}" --output /tmp/feishu_doc_out.txt
   ```

## 方式 D：上传文件

- PDF/图片：`Read` 工具直接读取
- 飞书消息 JSON：`python3 tools/feishu_parser.py --file {path} --target "{name}" --output /tmp/feishu_out.txt`
- 邮件 .eml/.mbox：`python3 tools/email_parser.py --file {path} --target "{name}" --output /tmp/email_out.txt`

## 方式 E：直接粘贴

用户粘贴内容直接作为文本原材料。
