# 人物技能项目

## 项目简介

这是一个使用 **huashu-nuwa** 技能蒸馏人物生成技能，使用 **skill-creator** 技能创建、优化、测试技能的项目。

## 目录结构

- **~/.claude/skills/**: 蒸馏生成的技能
- **~/skills/**: 优化后的技能
- **~/.evals/skills/**: 测试用例和输出结果
- **~/tools/**: 工具技能
  - **huashu-nuwa**: 女娲造人 - 人物蒸馏技能
  - **skill-creator**: 技能创建器 - 技能创建、优化和测试工具

## 技术栈

- 使用 **huashu-nuwa** 技能进行人物蒸馏
- 使用 **skill-creator** 技能进行技能创建、优化和测试

## 工具技能

### 1. huashu-nuwa（女娲造人）

**技能描述**：输入人名/主题/甚至只是模糊需求，自动深度调研→思维框架提炼→生成可运行的人物Skill。两种入口：(1)明确人名→直接蒸馏 (2)模糊需求→诊断推荐→再蒸馏。触发词：「造skill」「蒸馏XX」「女娲」「造人」「XX的思维方式」「做个XX视角」「更新XX的skill」。

**技能位置**：[tools/huashu-nuwa/](file:///workspace/tools/huashu-nuwa/)

**核心功能**：
- 人物深度调研
- 思维框架提炼
- 人物技能生成
- 模糊需求处理

### 2. skill-creator（技能创建器）

**技能描述**：创建新技能，修改和优化现有技能，测量技能性能。用于当用户想要从头创建技能、编辑或优化现有技能、运行评估来测试技能、用方差分析来基准测试技能性能或优化技能的描述以提高触发准确性时。

**技能位置**：[tools/skill-creator/](file:///workspace/tools/skill-creator/)

**核心功能**：
- 技能创建
- 技能优化
- 技能测试
- 性能基准
- 触发优化

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
