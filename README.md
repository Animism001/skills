# 人物技能项目

## 项目简介

这是一个使用 **huashu-nuwa** 技能蒸馏人物生成技能，使用 **skill-creator** 技能创建、优化、测试技能的项目。

## 目录结构

- **./.origin/skills/**: 蒸馏生成的初始技能
- **./.evals/skills/**: 测试用例和输出结果
- **./skills/**: 优化后的技能
- **./tools/**: 工具技能
  - **huashu-nuwa**: 女娲造人 - 人物蒸馏技能
  - **skill-creator**: 技能创建器 - 技能创建、优化和测试工具
  - **multi-search-engine**: 多搜索引擎集成 - 16个引擎（7个国内，9个国际）
  - **bilibili-search**: B站视频搜索 - 视频搜索、UP主信息查询
  - **youtube-transcript**: YouTube字幕获取 - 支持住宅IP代理
  - **bilibili-transcript**: B站字幕获取 - 支持CC/AI/Whisper三层回退
  - **web-researcher**: 网络研究工具 - 深度网页内容研究
  - **thinking-model-enhancer**: 思维模型增强器 - 思维框架优化
  - **literature-search**: 文学搜索 - 书籍和文献检索
  - **book-fetch**: 书籍获取 - 书籍内容检索

## 技术栈

- 使用 **huashu-nuwa** 技能进行人物蒸馏
- 使用 **skill-creator** 技能进行技能创建、优化和测试
- 使用 **multi-search-engine** 进行多源信息检索
- 使用 **youtube-transcript** / **bilibili-transcript** 获取视频字幕
- 使用 **bilibili-search** 搜索视频资源
- 使用 **web-researcher** 进行深度网络研究
- 使用 **thinking-model-enhancer** 优化思维框架
- 使用 **literature-search** / **book-fetch** 进行书籍文献检索

## 工具技能

### 1. huashu-nuwa（女娲造人）

**技能描述**：输入人名/主题/甚至只是模糊需求，自动深度调研→思维框架提炼→生成可运行的人物Skill。两种入口：(1)明确人名→直接蒸馏 (2)模糊需求→诊断推荐→再蒸馏。触发词：「造skill」「蒸馏XX」「女娲」「造人」「XX的思维方式」「做个XX视角」「更新XX的skill」。

**技能位置**：[tools/huashu-nuwa/](file:///workspace/tools/huashu-nuwa/)

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

**技能位置**：[tools/skill-creator/](file:///workspace/tools/skill-creator/)

**核心功能**：
- 技能创建（从零开始创建新技能）
- 技能优化（修改和提升现有技能）
- 技能测试（运行评估测试技能功能）
- 性能基准（用方差分析测试技能性能）
- 触发优化（优化技能描述提高触发准确性）

### 3. multi-search-engine（多搜索引擎集成）

**技能描述**：16个搜索引擎集成（7个国内，9个国际），支持高级搜索运算符、时间过滤、站点搜索、隐私引擎和WolframAlpha知识查询。无需API Key。

**技能位置**：[tools/multi-search-engine/](file:///workspace/tools/multi-search-engine/)

**核心功能**：
- 16个搜索引擎（百度、必应、Google、DuckDuckGo等）
- 高级搜索运算符支持
- 时间过滤和站点搜索
- 隐私引擎和知识查询

### 4. bilibili-search（B站视频搜索）

**技能描述**：搜索B站视频、获取UP主信息、查询热门视频，基于公开接口，无需API Key。

**技能位置**：[tools/bilibili-search/](file:///workspace/tools/bilibili-search/)

**核心功能**：
- 视频关键词搜索
- UP主信息查询
- 热门视频排行
- 视频详情获取

### 5. youtube-transcript（YouTube字幕获取）

**技能描述**：获取YouTube视频字幕，通过住宅IP代理，支持多种语言字幕。

**技能位置**：[tools/youtube-transcript/](file:///workspace/tools/youtube-transcript/)

**核心功能**：
- YouTube字幕获取
- 多语言字幕支持
- 住宅IP代理

### 6. bilibili-transcript（B站字幕获取）

**技能描述**：获取B站视频字幕，支持CC字幕、AI字幕、Whisper识别三层回退机制。

**技能位置**：[tools/bilibili-transcript/](file:///workspace/tools/bilibili-transcript/)

**核心功能**：
- B站字幕获取（CC/AI/Whisper三层回退）
- 自动字幕转换
- 多种格式输出

### 7. web-researcher（网络研究工具）

**技能描述**：深度网页内容研究，支持多页面分析、信息提取和综合报告生成。

**技能位置**：[tools/web-researcher/](file:///workspace/tools/web-researcher/)

**核心功能**：
- 深度网页内容分析
- 多源信息整合
- 研究报告生成

### 8. thinking-model-enhancer（思维模型增强器）

**技能描述**：优化和增强思维框架，提升心智模型、决策启发式和表达DNA的质量。

**技能位置**：[tools/thinking-model-enhancer/](file:///workspace/tools/thinking-model-enhancer/)

**核心功能**：
- 思维框架优化
- 决策模型增强
- 表达风格提炼

### 9. literature-search（文学搜索）

**技能描述**：搜索书籍和文献资源，支持多种数据库和检索方式。

**技能位置**：[tools/literature-search/](file:///workspace/tools/literature-search/)

**核心功能**：
- 书籍文献搜索
- 多数据库集成
- 高级检索功能

### 10. book-fetch（书籍获取）

**技能描述**：获取书籍内容和信息，支持多种格式和来源。

**技能位置**：[tools/book-fetch/](file:///workspace/tools/book-fetch/)

**核心功能**：
- 书籍内容检索
- 元数据获取
- 多格式支持

## Nuwa增强版工作流

为了提升人物蒸馏质量，我们设计了完整的**nuwa增强版工作流**，整合了所有新安装的工具技能。

### 工作流文档
详细工作流设计请查看：[nuwa-enhanced-workflow.md](file:///workspace/tools/nuwa-enhanced-workflow.md)

### 核心改进

1. **Phase 0（需求澄清）**：保持不变
2. **Phase 1（深度调研）**：重点强化
   - 使用multi-search-engine进行全网搜索
   - 使用bilibili-search搜索视频资源
   - 使用youtube-transcript和bilibili-transcript获取视频字幕
   - 使用web-researcher进行深度研究
   - 使用literature-search和book-fetch检索书籍文献

3. **Phase 2（思维框架提炼）**：重点强化
   - 使用thinking-model-enhancer优化思维框架
   - 应用三重验证方法论（跨域复现、生成力、排他性）

4. **Phase 3（Skill生成）**：保持不变
5. **Phase 4（质量验证）**：保持不变
6. **Phase 5（交付与更新）**：保持不变

### 使用示例

- **蒸馏Elon Musk**：用multi-search-engine搜索，用youtube-transcript获取访谈字幕
- **蒸馏中国人物**：用bilibili-search搜索，用bilibili-transcript获取字幕
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
