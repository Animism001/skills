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

| 角色 | 文件 | 职责 |
|------|------|------|
| **Researcher** 史料研究员 | `agents/researcher.md` | 获取历史事件、深度调研全部史实 |
| **Analyst** 深度分析师 | `agents/analyst.md` | D.E.S.I.R.E. Matrix 分析（事件+人物）、历史启示 |
| **PitchEditor** 选题编辑 | `agents/pitch-editor.md` | 基于Matrix分析选题、确定目标读者、提出创作要求、定制专属文风 |
| **CharacterDesigner** 人物设计师 | `agents/character-designer.md` | 基于Matrix分析创建人物设定、人物关系图谱 |
| **Architect** 故事架构师 | `agents/architect.md` | 整合素材设计故事大纲 |
| **Storyteller** 故事讲述者 | `agents/storyteller.md` | 根据所有素材创作最终故事 |
| **Editor** 史实审核员 | `agents/editor.md` | 审核史实准确性和叙事质量 |

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
      {event-slug}/                # 具体事件目录（仅入选事件）
        matrix.md                  # D.E.S.I.R.E. Matrix 分析 + 历史启示
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

对 events.md 中的**全部事件并行**进行深度调研，将结果保存到：
`./dayinhistory/{MM}/{DD}/{event-slug}/research.md`

不做筛选，全部调研。选题由选题组负责。

### Phase 3: D.E.S.I.R.E. Matrix 分析（Analyst，并行全部事件）

阅读 `agents/analyst.md` 获取详细指令。

对**全部事件**进行 D.E.S.I.R.E. Matrix 分析，两层分析：

**3a. 事件 Matrix 分析** - "这个事件为什么能流传千年"
- 保存到 `./history/{MM}/{DD}/{event-slug}/matrix.md`
- 包含：事件 Matrix、历史启示

**3b. 人物 Matrix 分析** - 对事件中的关键历史人物进行独立分析
- 识别事件中的所有关键人物
- 对每个人物进行 D.E.S.I.R.E. Matrix 分析
- 生成人物心理画像
- 保存到 `./history/{MM}/{DD}/{event-slug}/characters/{人物名}.md`

人物 Matrix 分析要点：
- D - Drive: 此人的核心驱动力是什么？（权力？安全？理想？）
- E - Experience: 此人在事件中扮演什么角色？
- S - Shortcut: 此人有哪些认知偏误？（如董卓的过度自信、吕布的锚定效应）
- I - Identity: 此人的身份原型是什么？（统治者？颠覆者？守护者？）
- R - Risk: 此人最恐惧什么？（失去权力？被背叛？遗臭万年？）
- E² - Emotion: 此人的情感弧线是什么？

### Phase 4: 选题与创作画像（PitchEditor）

阅读 `agents/pitch-editor.md` 获取详细指令。

选题编辑在 Matrix 分析之后介入，基于分析结果做出选题决策，输出两个文件：

1. **通读全部 research.md 和 matrix.md**，对当日所有历史事件及其心理密码形成全局理解
2. **选出 3-5 个**最值得创作故事的事件
3. **基于 D.E.S.I.R.E. Matrix 确定目标读者**：
   - 根据 E - Experience 分析读者代入的角色类型
   - 根据 I - Identity 分析触动的身份认同群体
   - 根据 E² - Emotion 分析偏好的情感弧线受众
4. **输出三合一创作画像** `profile.md`：
   - **[MATRIX]** - 从 Analyst 的 matrix.md 中提取精炼
   - **[WritingStyle]** - 基于 Matrix 二次推导专属文风（推导逻辑源自原始 JSON 设计）
   - **[剧情建议]** - 基于 Matrix 进行前瞻性剧情指导
5. **输出创作要求** `pitch.md`：
   - 选题理由、核心视角、情感定位、必须呈现的史实、认知偏误提醒、禁忌事项、字数建议

**选题逻辑**：不是选"最重要"的事件，而是选"最适合讲成故事"的事件。一个影响深远但缺乏人物张力的条约签署，不如一个影响较小但人物命运跌宕的小事件。

**WritingStyle 推导逻辑**（从原始 JSON 中提取的核心推导链）：
- D - Drive: 核心需求决定创作理念。追求"胜任感"→偏好"展现智识"，追求"归属感"→偏好"探索情感"
- E - Experience: 体验角色决定叙事节奏。"成就者"→快节奏行动，"探索者"→慢节奏描写，"社交家"→对话驱动
- S - Shortcut: 思维捷径决定复杂度。有"容忍模糊"偏误→能接受复杂情节，反之→简单直接
- I - Identity: 身份原型是语言风格关键。"智者"→思辨典雅，"颠覆者"→直接有冲击力
- R - Risk: 风险偏好影响描写精细度。害怕"模糊不清"→极度渴求微观精细描写
- E² - Emotion: 情感偏好决定核心基调。读者渴望的"情感终点"就是文风需要营造的最终氛围

### Phase 5: 人物设定与关系（CharacterDesigner，并行入选事件）

阅读 `agents/character-designer.md` 获取详细指令。

基于 Analyst 的人物 Matrix 分析，为每个关键人物创建：
- 人物设定卡片 → `./history/{MM}/{DD}/{event-slug}/characters/{人物名}.md`
- 人物关系图谱 → `./history/{MM}/{DD}/{event-slug}/relationships.md`

设计原则：
- 史实优先 - 核心性格和行为模式必须有史料支撑
- 矛盾立体 - 每个人物至少有一个核心矛盾
- 关系张力 - 人物之间必须有动态的张力关系
- 避免脸谱化 - 反派也有合理动机，英雄也有人性弱点

### Phase 6: 故事大纲（Architect，并行入选事件）

阅读 `agents/architect.md` 获取详细指令。

整合所有素材设计故事大纲：
- 读取 profile.md（创作画像）、pitch.md（创作要求）、research.md、matrix.md、characters/、relationships.md
- 设计场景序列、叙事视角、情感弧线
- 保存到 `./history/{MM}/{DD}/{event-slug}/outline.md`

### Phase 7: 故事创作（Storyteller，并行入选事件）

阅读 `agents/storyteller.md` 获取详细指令。

**Storyteller 不直出故事，而是读取所有素材后创作**：
- 读取 profile.md（创作画像：Matrix+WritingStyle+剧情建议）、pitch.md（创作要求）、research.md、matrix.md、characters/、relationships.md、outline.md
- 严格按照专属文风和人物设定创作
- 保存到 `./history/{MM}/{DD}/{event-slug}/story.md`

### Phase 8: 史实审核（Editor）

阅读 `agents/editor.md` 获取详细指令。

对照 research.md 审核故事的史实准确性和叙事质量：
- 保存审核结果到 `./history/{MM}/{DD}/{event-slug}/review.md`
- 如有重大史实错误，返回 Storyteller 修改

## 并行策略

整个工作流中，以下环节可以并行处理：

1. **Phase 1** - 多个数据源并行请求
2. **Phase 2** - 全部事件并行调研
3. **Phase 3** - 全部事件并行分析（事件Matrix + 人物Matrix）
4. **Phase 5** - 入选事件并行设计人物
5. **Phase 6** - 入选事件并行设计大纲
6. **Phase 7** - 入选事件并行创作故事

使用 Task 工具启动子代理时，同一 Phase 内的多个事件应并行启动。

## 数据获取脚本

```bash
python scripts/fetch_history.py [--month M] [--day D] [--output OUTPUT]
```

脚本会并行请求多个数据源，合并去重后输出 JSON 格式的事件列表。

## 参考文件

- `references/desire-matrix.md` - D.E.S.I.R.E. Matrix 完整理论框架与文风定制模板
- `agents/researcher.md` - 史料研究员角色定义
- `agents/analyst.md` - 深度分析师角色定义
- `agents/pitch-editor.md` - 选题编辑角色定义
- `agents/character-designer.md` - 人物设计师角色定义
- `agents/architect.md` - 故事架构师角色定义
- `agents/storyteller.md` - 故事讲述者角色定义
- `agents/editor.md` - 史实审核员角色定义
