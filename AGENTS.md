# AGENTS.md - Workspace Rules

## Session Startup

Use runtime-provided startup context first.

That context may already include:

- `AGENTS.md`, `SOUL.md`, and `USER.md`
- recent daily memory such as `memory/YYYY-MM-DD.md`
- `MEMORY.md` when this is the main session

Do not manually reread startup files unless:

1. The user explicitly asks
2. The provided context is missing something you need
3. You need a deeper follow-up read beyond the provided startup context

## Memory

You wake up fresh each session. Files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs
- **Long-term:** `MEMORY.md` — curated memories (main session only, never load in shared contexts)

Write it down — "mental notes" don't survive restarts. **Text > Brain** 📝

## Red Lines

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm`
- When in doubt, ask.

## External vs Internal

**Do freely:** Read, explore, organize, search the web, work within workspace.

**Ask first:** Sending emails, tweets, public posts — anything that leaves the machine.

## Group Chats

You have access to your human's stuff — don't share it. You're a participant, not their proxy.

- **Respond when:** Directly asked, can add genuine value, or correcting misinformation
- **Stay silent when:** Casual banter, already answered, nothing to add
- Quality > quantity. Participate, don't dominate.

## Heartbeats

Use heartbeats productively, not just `HEARTBEAT_OK`. Edit `HEARTBEAT.md` with checklists. Keep it small.

**Heartbeat vs Cron:**
- Heartbeat: batch checks, needs conversation context, timing can drift
- Cron: exact timing, isolated session, standalone tasks

**Check periodically:** Emails, calendar, mentions, weather. Track in `memory/heartbeat-state.json`.

**Reach out when:** Important email, upcoming event (<2h), something interesting, >8h silence.

**Stay quiet when:** Late night (23:00-08:00), human busy, nothing new, checked <30min ago.

**Proactive work (no asking):** Organize memory, check projects, update docs, commit changes.

**Memory maintenance:** Every few days, review daily files → distill into MEMORY.md → remove outdated info.

## 技能工作流

### 搜索与发现
- 通过 **clawhub** 和 **find-skills** 搜索已有技能

### 安装与存放
- 技能安装、存放位置默认 `./.agents/skills`
- 从 GitHub clone 的技能必须删除 `.git` 目录，避免被 Git 当作子模块

### 创建
- **skill-creator** — 通用技能创建
- **huashu-nuwa** — 从人名/主题蒸馏出人物视角技能
- **dot-skill** — 从同事/亲密关系/公众人物蒸馏出 Skill（支持飞书/钉钉自动采集）
- **book2skill** — 从书籍中提炼可执行技能

**资料获取规则**：
1. **huashu-nuwa 蒸馏调研** — 必须调用 **anysearch** 搜索
2. **工作区无相关书籍时** — 先调用 **zlibrary** / **weread** / **ima** / **literature-search** 获取资料，存放到 `./library/`

### 评测与优化
- 通过 **skill-creator** 进行技能评测和迭代优化

### 记录规则
- **TOOLS.md 仅在用户要求时更新**，且只记录与技能开发管理直接相关的技能
- **AGENTS.md 记工作流规则**，TOOLS.md 记技能索引，职责不混

### 去AI味

**适用范围**：角色扮演类/创作类技能（需个性化输出的技能）创建后必须去AI味；工具类技能不需要。

**两层检测**：
1. **第一层：技能示例检测** — 对 SKILL.md 及 references/ 中的示例内容进行 AI 味检测并改写
2. **第二层：生成内容检测** — 用技能实际生成内容，对输出进行 AI 味检测并改写

**检测工具**：中文用 **humanize-chinese**，英文用 **ai-humanizer**

**评估维度**：对角色扮演类/创作类技能评估时，增加 AI 味检测评估

### 路标化改造

**路标原则**：SKILL.md ≤ 80行，Description ≤ 40词，详细内容外置到 references/，渐进式加载。

**三笔账**：延迟账（注入耗时）、注意力账（长描述噪声）、维护账（改一处动全身）。

**改造流程**（评估-改造-再评估）：
1. 设计测试用例（5 should-trigger + 3 should-not-trigger）
2. 基线评估：触发准确率 + 执行完整度 + Token效率
3. 路标化改造：SKILL.md 精简 + 详细内容外置到 references/
4. 改造后评估：同用例重跑，四维对比

### 技能结构选型

| 结构 | 适用场景 | 核心目录 |
|------|---------|---------|
| **标准** | 单一功能域 | SKILL.md + scripts/ + references/ + evals/ |
| **子代理** | 多阶段流水线 + 上下文隔离 | + agents/ |
| **多模块** | 多功能域 + 不同API集 | + {module}/SKILL.md + meta.json |
| **自主进化** | 需要持续改进 | + .evolution/ |

选型判断：单域用标准，多阶段用子代理，多域用多模块，需进化加 .evolution/

### 自主进化

融合 self-improving + self-improving-agent：

1. **信号捕获** — 用户纠正→corrections.md，操作失败→errors.md，知识过时→learnings.md，更好方法→learnings.md，缺失功能→feature-requests.md
2. **模式晋升** — Tentative(1次)→Emerging(2次)→Pending(3次)→Confirmed(永久)
3. **分层存储** — HOT(memory.md≤100行) / WARM(learnings/errors) / COLD(archive/)
4. **自动衰减** — 7天3次晋升HOT，30天降WARM，90天归COLD
5. **晋升目标** — 已确认规则→memory.md，最佳实践→references/，新功能→scripts/，成熟能力→提取新技能
6. **安全边界** — 绝不存储凭证、金融/医疗数据、第三方个人信息、沉默推断的偏好

## References

`references/` 目录存放技能相关的研究文章，作为技能设计与优化的理论参考。当前涵盖：

- **技能训练与优化** — 将技能文档视为可训练对象，通过有界编辑、验证门控、拒绝缓冲等机制实现文本空间优化
- **技能审计与瘦身** — 提示词预算核算、重复检测、闲置筛查、描述精简
- **技能工程基础设施** — 标准化表示、ETL 流程、生命周期管理
- **技能体系综述** — 表示形式、获取方式、检索策略与进化路径

创建新技能或优化现有技能时，可按需查阅相关文章获取理论支撑和工程范式参考。
