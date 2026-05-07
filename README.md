# 人物技能项目

## 项目简介

这是一个使用 **huashu-nuwa** 技能蒸馏人物生成技能，使用 **skill-creator** 技能创建、优化、测试技能的项目。

## 目录结构

- **./.origin/skills/**: 蒸馏生成的初始技能
- **./.evals/skills/**: 测试用例和输出结果
- **./skills/**: 技能目录
  - **robert-mckee-perspective/**: 示例人物技能
  - **huashu-nuwa/**: 女娲造人 - 人物蒸馏技能
  - **skill-creator/**: 技能创建器 - 技能创建、优化和测试工具
  - **multi-search-engine/**: 多搜索引擎集成 - 16个引擎（7个国内，9个国际）
  - **zlibrary/**: Z-Library书籍获取 - 电子书搜索和下载
  - **literature-search/**: 文学搜索 - 书籍和文献检索
  - **book-fetch/**: 书籍获取 - 电子书获取（Anna's Archive）
  - **bilibili-search/**: B站视频搜索 - 视频搜索、UP主信息查询
  - **bilibili-transcript/**: B站字幕获取 - 支持CC/AI/Whisper三层回退
  - **youtube-transcript/**: YouTube字幕获取 - 支持住宅IP代理
  - **web-researcher/**: 网络研究工具 - 深度网页内容研究
  - **thinking-model-enhancer/**: 思维模型增强器 - 思维框架优化
  - **self-improving/**: 自我优化工具
  - **self-improving-agent/**: 自我优化Agent
  - **inkos/**: 小说写作技能
  - **ima-skill/**: 腾讯IMA知识库管理

## 技术栈

- 使用 **huashu-nuwa** 技能进行人物蒸馏
- 使用 **skill-creator** 技能进行技能创建、优化和测试
- 使用 **multi-search-engine** 进行多源信息检索
- 使用 **zlibrary** / **book-fetch** 获取电子书
- 使用 **literature-search** 搜索学术文献
- 使用 **youtube-transcript** / **bilibili-transcript** 获取视频字幕
- 使用 **bilibili-search** 搜索视频资源
- 使用 **web-researcher** 进行深度网络研究
- 使用 **thinking-model-enhancer** 优化思维框架
- 使用 **ima-skill** 管理笔记和知识库

## 工具技能

### 1. huashu-nuwa（女娲造人）

**技能描述**：输入人名/主题/甚至只是模糊需求，自动深度调研→思维框架提炼→生成可运行的人物Skill。两种入口：(1)明确人名→直接蒸馏 (2)模糊需求→诊断推荐→再蒸馏。触发词：「造skill」「蒸馏XX」「女娲」「造人」「XX的思维方式」「做个XX视角」「更新XX的skill」。

**技能位置**：[skills/huashu-nuwa/](file:///workspace/skills/huashu-nuwa/)

**核心功能**：
- 多源信息采集（6个并行Agent）
- 思维框架提炼（心智模型、决策启发式、表达DNA）
- 人物技能生成（完整的SKILL.md结构）
- 质量验证（已知测试、边缘测试、风格测试）
- 技能更新（增量更新已有Skill）

**项目特色**：
- 完整的5阶段执行流程
- 支持本地语料优先模式
- 信息源优先级和黑名单管理
- 双Agent精炼工序
- 多种特殊场景处理（主题Skill、中国人物、冷门人物等）

### 2. skill-creator（技能创建器）

**技能描述**：创建新技能，修改和优化现有技能，测量技能性能。用于当用户想要从头创建技能、编辑或优化现有技能、运行评估来测试技能、用方差分析来基准测试技能性能或优化技能的描述以提高触发准确性时。

**技能位置**：[skills/skill-creator/](file:///workspace/skills/skill-creator/)

**核心功能**：
- 技能创建（从零开始创建新技能）
- 技能优化（修改和提升现有技能）
- 技能测试（运行评估测试技能功能）
- 性能基准（用方差分析测试技能性能）
- 触发优化（优化技能描述提高触发准确性）

### 3. multi-search-engine（多搜索引擎集成）

**技能描述**：16个搜索引擎集成（7个国内，9个国际），支持高级搜索运算符、时间过滤、站点搜索、隐私引擎和WolframAlpha知识查询。无需API Key。

**技能位置**：[skills/multi-search-engine/](file:///workspace/skills/multi-search-engine/)

**核心功能**：
- 16个搜索引擎（百度、必应、Google、DuckDuckGo等）
- 高级搜索运算符支持
- 时间过滤和站点搜索
- 隐私引擎和知识查询

### 4. zlibrary（Z-Library书籍获取）

**技能描述**：搜索和下载电子书，支持多种格式，是人物蒸馏中获取著作资料的首选工具。

**技能位置**：[skills/zlibrary/](file:///workspace/skills/zlibrary/)

**核心功能**：
- 电子书搜索和下载
- 多种格式支持
- 海量图书资源库

### 5. literature-search（文学搜索）

**技能描述**：搜索书籍和文献资源，支持多种数据库和检索方式，包括Google Scholar、PubMed、arXiv等学术数据库。

**技能位置**：[skills/literature-search/](file:///workspace/skills/literature-search/)

**核心功能**：
- 书籍文献搜索
- 多数据库集成（Google Scholar、PubMed、arXiv等）
- 高级检索功能

### 6. book-fetch（书籍获取）

**技能描述**：获取书籍内容和信息，支持多种格式和来源，通过Anna's Archive获取电子书。

**技能位置**：[skills/book-fetch/](file:///workspace/skills/book-fetch/)

**核心功能**：
- 电子书获取（Anna's Archive）
- 元数据获取
- 多格式支持

### 7. bilibili-search（B站视频搜索）

**技能描述**：搜索B站视频、获取UP主信息、查询热门视频，基于公开接口，无需API Key。

**技能位置**：[skills/bilibili-search/](file:///workspace/skills/bilibili-search/)

**核心功能**：
- 视频关键词搜索
- UP主信息查询
- 热门视频排行
- 视频详情获取
- 获取UP主所有视频列表

### 8. bilibili-transcript（B站字幕获取）

**技能描述**：获取B站视频字幕，支持CC字幕、AI字幕、Whisper识别三层回退机制。

**技能位置**：[skills/bilibili-transcript/](file:///workspace/skills/bilibili-transcript/)

**核心功能**：
- B站字幕获取（CC/AI/Whisper三层回退）
- 自动字幕转换
- 多种格式输出

### 9. youtube-transcript（YouTube字幕获取）

**技能描述**：获取YouTube视频字幕，通过住宅IP代理，支持多种语言字幕。

**技能位置**：[skills/youtube-transcript/](file:///workspace/skills/youtube-transcript/)

**核心功能**：
- YouTube字幕获取
- 多语言字幕支持
- 住宅IP代理

### 10. web-researcher（网络研究工具）

**技能描述**：深度网页内容研究，支持多页面分析、信息提取和综合报告生成。

**技能位置**：[skills/web-researcher/](file:///workspace/skills/web-researcher/)

**核心功能**：
- 深度网页内容分析
- 多源信息整合
- 研究报告生成

### 11. thinking-model-enhancer（思维模型增强器）

**技能描述**：优化和增强思维框架，提升心智模型、决策启发式和表达DNA的质量。

**技能位置**：[skills/thinking-model-enhancer/](file:///workspace/skills/thinking-model-enhancer/)

**核心功能**：
- 思维框架优化
- 决策模型增强
- 表达风格提炼

### 12. self-improving（自我优化）

**技能描述**：排行榜第1名的自我优化技能，持续改进Agent能力。

**技能位置**：[skills/self-improving/](file:///workspace/skills/self-improving/)

### 13. self-improving-agent（自我优化Agent）

**技能描述**：排行榜第3名的自我优化Agent技能。

**技能位置**：[skills/self-improving-agent/](file:///workspace/skills/self-improving-agent/)

### 14. inkos（小说写作）

**技能描述**：专业的小说写作技能，支持多种类型和风格。

**技能位置**：[skills/inkos/](file:///workspace/skills/inkos/)

### 15. ima-skill（IMA知识库）

**技能描述**：腾讯IMA的统一API技能，支持笔记管理和知识库操作。

**技能位置**：[skills/ima-skill/](file:///workspace/skills/ima-skill/)

## Nuwa增强版工作流

为了提升人物蒸馏质量，我们设计了完整的**nuwa增强版工作流**，整合了所有新安装的工具技能。

### 工作流文档
详细工作流设计请查看：[nuwa-enhanced-workflow.md](file:///workspace/skills/nuwa-enhanced-workflow.md)

### 核心改进

1. **Phase 0（需求分析与分流）**：保持不变
   - 增强：使用`thinking-model-enhancer`辅助需求诊断

2. **Phase 1（多源信息采集 - 6个并行Agent）**：重点强化
   - **Agent 1（著作调研）**：multi-search-engine + zlibrary + literature-search + web-researcher
   - **Agent 2（对话调研）**：multi-search-engine + bilibili-search + bilibili-transcript + youtube-transcript
   - **Agent 3（表达风格调研）**：multi-search-engine + web-researcher
   - **Agent 4（他者视角调研）**：multi-search-engine + web-researcher
   - **Agent 5（决策调研）**：multi-search-engine + web-researcher
   - **Agent 6（时间线调研）**：multi-search-engine + web-researcher

3. **Phase 1.5（调研质量检查）**：新增
   - 使用`merge_research.py`生成摘要表格
   - 增强：使用`thinking-model-enhancer`初步评估信息质量

4. **Phase 2（思维框架提炼）**：重点强化
   - 使用`thinking-model-enhancer`优化思维框架
   - 应用三重验证方法论（跨域复现、生成力、排他性）

5. **Phase 3-4（Skill构建与质量验证）**：保持不变
   - 增强：使用`skill-creator`辅助构建标准化Skill
   - 增强：使用`thinking-model-enhancer`优化Skill内容

6. **Phase 5（双Agent精炼）**：增强
   - `thinking-model-enhancer`作为Agent A（优化视角）
   - `skill-creator`作为Agent B（Skill构建视角）

### 技能调用优先级

| 维度 | 首选技能 | 次选技能 | 备选技能 |
|------|---------|---------|---------|
| **通用搜索** | multi-search-engine | web-researcher | — |
| **书籍获取** | zlibrary | book-fetch | literature-search |
| **文献搜索** | literature-search | multi-search-engine | — |
| **B站视频** | bilibili-search | multi-search-engine | — |
| **B站字幕** | bilibili-transcript | — | — |
| **YouTube字幕** | youtube-transcript | — | — |

### 使用示例

- **蒸馏Elon Musk**：multi-search-engine + zlibrary + youtube-transcript
- **蒸馏中国人物**：multi-search-engine(国内引擎) + zlibrary + bilibili-search + bilibili-transcript
- **模糊需求**：先诊断推荐，再按强化流程执行

## 当前技能列表

### 1. robert-mckee-perspective

**技能描述**：提供罗伯特·麦基（Robert McKee）的故事理论和观点分析。当用户询问关于故事结构、编剧技巧、叙事理论、人物塑造、对白设计等与麦基理论相关的问题时，使用此技能。

**技能位置**：[skills/robert-mckee-perspective/](file:///workspace/skills/robert-mckee-perspective/)

**测试用例**：[.evals/skills/robert-mckee-perspective/](file:///workspace/.evals/skills/robert-mckee-perspective/)

**核心功能**：
- 故事结构分析
- 人物塑造指导
- 对白设计建议
- 叙事原理解释
- 案例分析
- 商业故事应用
