---
name: history-story
description: 历史故事创作技能。当用户要求创作历史故事、了解"历史上的今天"、将历史事件改编为故事、或提到"历史故事"、"今天的历史"、"历史上的今天"、"写一个历史故事"时使用此技能。即使用户只是说"今天历史上发生了什么"或"给我讲一个历史故事"，也应触发。此技能会先调研历史上的今天发生的事件，再深入调研具体史实，用D.E.S.I.R.E. Matrix分析事件与人物，然后由选题组基于分析结果选出最有故事价值的事件、确定目标读者并提出创作要求，生成人物设定和故事大纲，最后交由Storyteller子代理创作引人入胜的历史故事。
---

# history-story 历史故事创作技能

## 核心理念

历史不是冰冷的时间线，而是无数鲜活生命的抉择与命运。本技能将历史事件转化为引人入胜的故事，让读者在沉浸式阅读中自然领悟历史智慧——不直接说教，而是让故事本身成为最好的老师。

为什么有些历史事件能流传千年？因为它们触及了人类最深层的情感与困境。本技能用 D.E.S.I.R.E. Matrix 解码这些事件和人物背后的心理密码，为每个故事定制专属文风和人物设定。

## 团队架构

本技能采用团队协作模式，每个阶段由专门的子代理负责：

| 角色 | 文件 | 职责 | 处理范围 |
|------|------|------|----------|
| **Researcher** 史料研究员 | `agents/researcher.md` | 获取历史事件、深度调研史实 | 单事件 |
| **Analyst** 深度分析师 | `agents/analyst.md` | D.E.S.I.R.E. Matrix 分析（事件+人物） | 单事件 |
| **Evaluator** 事件评估员 | `agents/evaluator.md` | 轻量级评估，输出评估卡片 | 单事件 |
| **Selector** 选题决策 | 由主控代理执行 | 读取评估卡片，选出3-5个事件 | 仅读eval-card |
| **PitchEditor** 选题编辑 | `agents/pitch-editor.md` | 三合一创作画像 + 创作要求 | 单事件（仅入选） |
| **CharacterDesigner** 人物设计师 | `agents/character-designer.md` | 人物设定、人物关系图谱 | 单事件（仅入选） |
| **Architect** 故事架构师 | `agents/architect.md` | 整合素材设计故事大纲 | 单事件（仅入选） |
| **Storyteller** 故事讲述者 | `agents/storyteller.md` | 根据素材创作最终故事 | 单事件（仅入选） |
| **Editor** 史实审核员 | `agents/editor.md` | 审核史实准确性和叙事质量 | 单事件（仅入选） |

## 上下文控制原则

**核心规则：每个子代理只处理一个事件，只读取该事件的文件，绝不跨事件读取。**

这样可以：
1. 避免上下文爆炸（20+事件的素材远超上下文窗口）
2. 避免上下文污染（不同事件的信息互相干扰）
3. 支持并行处理（每个子代理独立运行）

唯一需要跨事件读取的是 Selector 步骤，但它只读取紧凑的 eval-card.md（每张约200字），而非完整素材。

## 目录结构

```
./dayinhistory/                    # 原始历史事件数据
  {MM}/                            # 两位数月份（如 05）
    {DD}/                          # 两位数日期（如 22）
      events.md                    # 当日所有历史事件概览
      {event-slug}/                # 具体事件调研目录
        research.md                # 史实调研结果

./history/                         # 创作素材与成品
  {MM}/                            # 两位数月份
    {DD}/                          # 两位数日期
      selection.md                 # 选题结果（入选事件列表）
      {event-slug}/                # 具体事件目录
        matrix.md                  # D.E.S.I.R.E. Matrix 分析 + 历史启示
        eval-card.md               # 评估卡片（轻量级，供Selector读取）
        profile.md                 # 三合一创作画像：Matrix + WritingStyle + 剧情建议
        pitch.md                   # 创作要求
        characters/                # 人物设定
          {人物名}.md              # 单个人物的设定卡片
        relationships.md           # 人物关系图谱
        outline.md                 # 故事大纲
        story.md                   # 最终故事
        review.md                  # 审核报告
```

`{event-slug}` 命名规则：`{年份}-{事件简称}`，如 `192-董卓被诛`、`1945-广岛原子弹`。

## 工作流程

### Phase 1: 获取历史事件（Researcher，并行数据源）

阅读 `agents/researcher.md` 获取详细指令。

1. 运行 `scripts/fetch_history.py` 获取当日历史事件
2. 使用 WebSearch 补充搜索（`历史上的今天 {M}月{D}日 重大事件`、`today in history {month} {day}`）
3. 将事件列表保存到 `./dayinhistory/{MM}/{DD}/events.md`

### Phase 2: 深度史实调研（Researcher，并行全部事件）

阅读 `agents/researcher.md` 获取详细指令。

对 events.md 中的**全部事件并行**进行深度调研。每个子代理只处理一个事件，将结果保存到：
`./dayinhistory/{MM}/{DD}/{event-slug}/research.md`

### Phase 3: D.E.S.I.R.E. Matrix 分析（Analyst，并行全部事件）

阅读 `agents/analyst.md` 获取详细指令。

对**全部事件并行**进行 D.E.S.I.R.E. Matrix 分析。每个子代理只处理一个事件：

**3a. 事件 Matrix 分析** → `./history/{MM}/{DD}/{event-slug}/matrix.md`
**3b. 人物 Matrix 分析** → `./history/{MM}/{DD}/{event-slug}/characters/{人物名}.md`

### Phase 4a: 事件评估（Evaluator，并行全部事件）

阅读 `agents/evaluator.md` 获取详细指令。

对**全部事件并行**进行轻量级评估。每个子代理只处理一个事件，只读取该事件的 research.md + matrix.md + characters/，输出紧凑的评估卡片：
`./history/{MM}/{DD}/{event-slug}/eval-card.md`

评估卡片包含：基本信息、故事潜力评分（5维度）、关键人物（最多3个）、Matrix核心发现（最多3条）、目标读者预判。每张卡片约200字，便于后续横向比较。

### Phase 4b: 选题决策（Selector，由主控代理执行）

**此步骤不由子代理执行，而由主控代理直接执行**，因为只需读取紧凑的 eval-card.md 文件。

1. 读取 `./history/{MM}/{DD}/{event-slug}/eval-card.md`（所有事件）
2. 基于评估卡片的评分和简评，选出 3-5 个最值得创作故事的事件
3. 选题标准：
   - 综合评分最高
   - 中外均衡（避免全是同一地区/时代）
   - 主题多样性（避免全是战争或全是政治）
4. 保存选题结果到 `./history/{MM}/{DD}/selection.md`

selection.md 格式：
```markdown
# {M}月{D}日 选题结果

## 入选事件
| # | 年份 | 事件 | 综合评分 | 选题理由 |
|---|------|------|----------|----------|
| 1 | {year} | {title} | ⭐{N} | {一句话理由} |
| 2 | {year} | {title} | ⭐{N} | {一句话理由} |
| 3 | {year} | {title} | ⭐{N} | {一句话理由} |

## 未入选事件
| 年份 | 事件 | 综合评分 | 未入选原因 |
|------|------|----------|-----------|
| {year} | {title} | ⭐{N} | {原因} |
```

### Phase 4c: 创作画像与要求（PitchEditor，并行入选事件）

阅读 `agents/pitch-editor.md` 获取详细指令。

对**入选事件并行**处理。每个子代理只处理一个事件，只读取该事件的素材，输出两个文件：

1. **profile.md** - 三合一创作画像：
   - **[MATRIX]** - 从 matrix.md 中提取精炼
   - **[WritingStyle]** - 基于 Matrix 二次推导专属文风
   - **[剧情建议]** - 基于 Matrix 进行前瞻性剧情指导

2. **pitch.md** - 创作要求

**WritingStyle 推导逻辑**（源自原始 JSON 设计）：
- D - Drive: 核心需求决定创作理念。追求"胜任感"→偏好"展现智识"，追求"归属感"→偏好"探索情感"
- E - Experience: 体验角色决定叙事节奏。"成就者"→快节奏行动，"探索者"→慢节奏描写，"社交家"→对话驱动
- S - Shortcut: 思维捷径决定复杂度。有"容忍模糊"偏误→能接受复杂情节，反之→简单直接
- I - Identity: 身份原型是语言风格关键。"智者"→思辨典雅，"颠覆者"→直接有冲击力
- R - Risk: 风险偏好影响描写精细度。害怕"模糊不清"→极度渴求微观精细描写
- E² - Emotion: 情感偏好决定核心基调。读者渴望的"情感终点"就是文风需要营造的最终氛围

### Phase 5: 人物设定与关系（CharacterDesigner，并行入选事件）

阅读 `agents/character-designer.md` 获取详细指令。

每个子代理只处理一个事件，只读取该事件的 characters/ 目录和 research.md：
- 人物设定卡片 → `characters/{人物名}.md`
- 人物关系图谱 → `relationships.md`

**上下文控制**：如果事件人物超过5个，只为主要人物（与核心冲突最直接相关的3-5人）创建完整设定卡片，次要人物在 relationships.md 中简要描述。

### Phase 6: 故事大纲（Architect，并行入选事件）

阅读 `agents/architect.md` 获取详细指令。

每个子代理只处理一个事件。**读取优先级**：
1. **必读**：profile.md（创作画像）、pitch.md（创作要求）、outline.md 自身
2. **按需读取**：research.md（查史实）、characters/（查人物）、relationships.md（查关系）
3. **不需要读取**：matrix.md（已被 profile.md 精炼包含）

设计场景序列、叙事视角、情感弧线，保存到 `outline.md`。

### Phase 7: 故事创作（Storyteller，并行入选事件）

阅读 `agents/storyteller.md` 获取详细指令。

每个子代理只处理一个事件。**读取优先级**：
1. **必读**：outline.md（故事骨架）、profile.md（文风+剧情建议）、pitch.md（创作要求）
2. **按需读取**：characters/ 中主要人物的设定卡片、relationships.md
3. **不需要读取**：research.md（史实已在 outline.md 的注记中）、matrix.md（已被 profile.md 包含）

严格按照专属文风和人物设定创作，保存到 `story.md`。

### Phase 8: 史实审核（Editor，并行入选事件）

阅读 `agents/editor.md` 获取详细指令。

每个子代理只处理一个事件，只读取 story.md + research.md + outline.md 中的史实注记，保存审核结果到 `review.md`。

## 并行策略

整个工作流中，以下环节可以并行处理：

1. **Phase 1** - 多个数据源并行请求
2. **Phase 2** - 全部事件并行调研（每个子代理1个事件）
3. **Phase 3** - 全部事件并行分析（每个子代理1个事件）
4. **Phase 4a** - 全部事件并行评估（每个子代理1个事件）
5. **Phase 4c** - 入选事件并行输出创作画像（每个子代理1个事件）
6. **Phase 5** - 入选事件并行设计人物（每个子代理1个事件）
7. **Phase 6** - 入选事件并行设计大纲（每个子代理1个事件）
8. **Phase 7** - 入选事件并行创作故事（每个子代理1个事件）
9. **Phase 8** - 入选事件并行审核（每个子代理1个事件）

使用 Task 工具启动子代理时，同一 Phase 内的多个事件应并行启动。每个子代理的任务描述中必须明确指定其处理的事件 slug 和可读取的文件范围。

## 数据获取脚本

```bash
python scripts/fetch_history.py [--month M] [--day D] [--output OUTPUT]
```

## 参考文件

- `references/desire-matrix.md` - D.E.S.I.R.E. Matrix 完整理论框架与文风定制模板
- `agents/researcher.md` - 史料研究员角色定义
- `agents/analyst.md` - 深度分析师角色定义
- `agents/evaluator.md` - 事件评估员角色定义
- `agents/pitch-editor.md` - 选题编辑角色定义
- `agents/character-designer.md` - 人物设计师角色定义
- `agents/architect.md` - 故事架构师角色定义
- `agents/storyteller.md` - 故事讲述者角色定义
- `agents/editor.md` - 史实审核员角色定义
