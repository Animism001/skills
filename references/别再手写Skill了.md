# 别再手写Skill了！微软最新研究：像神经网络一样训练Skill

**论文标题**：SkillOpt: Executive Strategy for Self-Evolving Agent Skills

**作者**：Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, Chong Luo

**发表位置**：arXiv preprint (2605.23904)，微软、上海交通大学、同济大学、复旦大学

**代码地址**：https://github.com/microsoft/SkillOpt

## 1. 论文要解决什么问题？

随着大语言模型逐渐从"回答问题"走向"执行任务"，Agent 的能力不再只取决于模型权重本身，还取决于它如何调用工具、搜索证据、读取文件、验证中间结果、遵守输出格式，以及避免重复犯错。论文把这些可复用的程序性知识称为 **agent skill**：它通常是一个自然语言文档，包含任务流程、领域启发式、工具使用策略、输出约束和失败模式等内容。

过去的 skill 主要有三种来源：人工编写、让 LLM 一次性生成、或者让 Agent 根据失败经验自我修改。论文认为，这些方法虽然能带来一定收益，但缺少类似深度学习训练中的稳定机制：没有清晰的训练状态，没有受控的更新步长，没有验证集筛选，也没有对失败更新的记录。因此，skill 容易出现"看起来合理，但实际效果变差"的问题。

SkillOpt 的核心目标就是解决这个问题：**把 skill 文档本身当作冻结模型之外的可训练对象**。模型参数不更新，执行环境不改变，优化的对象只是一个可读、可审计、可迁移的文本文件。

## 2. 背景直觉：为什么 skill 需要"训练"？

在传统深度学习中，模型通过多轮训练不断调整参数；每一步更新都会受到 batch、learning rate、validation 等机制控制。SkillOpt 借用了这个思想，但它不是在权重空间里优化参数，而是在文本空间里优化 skill 文档。

| 深度学习训练概念 | SkillOpt 中的对应物 |
|---|---|
| 模型参数 | skill document |
| 梯度方向 | 从执行轨迹中总结出的编辑方向 |
| learning rate | 每一步允许修改多少条文本规则 |
| batch / minibatch | rollout batch 和 reflection minibatch |
| validation set | held-out selection split |
| optimizer state | 当前 skill、最佳 skill、被拒绝编辑、meta skill |
| checkpoint | `best_skill.md` |

SkillOpt 不允许优化器随意重写整个 skill，而是要求每次修改都有 evidence、有边界、有验证、有拒绝机制。论文把这种方法称为 **controllable text-space optimizer**。

## 3. 方法概述：SkillOpt 的整体流程

SkillOpt 的流程可以概括为五步：

1. 冻结目标模型带着当前 skill 执行一批任务；
2. 系统记录执行轨迹、工具调用、最终答案和 verifier 分数；
3. 优化器模型阅读成功和失败轨迹，提出 skill 编辑建议；
4. 系统根据文本学习率预算，只应用有限数量的 add/delete/replace 编辑；
5. 候选 skill 必须在 held-out validation split 上严格提升，才会被接受。

最终部署时，只导出一个 compact 的 `best_skill.md`。目标模型不需要额外推理调用，也不需要权重更新。论文报告最终 skill 通常只有约 300–2,000 tokens，并且只经过 1–4 次被接受的编辑。

## 4. 关键设计细节

### 4.1 Rollout Evidence：先让模型带着 skill 做任务

在每个优化 step 中，目标模型会带着当前 skill 在训练任务上执行。系统会记录任务元信息、对话消息、工具调用、观察结果、命令输出、最终答案、verifier feedback，以及 benchmark 相关上下文。这一步相当于深度学习中的 forward pass。

### 4.2 Minibatch Reflection：用成功和失败轨迹生成编辑方向

优化器模型不是直接执行任务，而是阅读执行轨迹。SkillOpt 会把成功样本和失败样本分开，再组成 reflection minibatch。失败 minibatch 暴露反复出现的系统性错误，成功 minibatch 保留已经有效的行为模式。每个 minibatch 返回结构化的 add / delete / replace 编辑。

### 4.3 编辑预算（文本学习率）

合并后的编辑池被 optimizer 按预期效用排序，然后截断到预算上限（比如每步最多改 4 条规则）。这是和无约束重写的关键区别：有界更新保持连续性，每一版 skill 和上一版足够接近。

### 4.4 验证门控

每个候选 skill 必须在 held-out 验证集上严格提升才会被接受。被拒绝的编辑不会丢弃，而是存入 rejected-edit buffer，供后续反思参考。

### 4.5 慢速更新与 Meta Skill

epoch 边界上的 slow/meta update 从相邻 epoch 学习：把同一批训练样本在上一 epoch 和当前 epoch 的 skill 下分别跑一遍，划分成进步、退步、持续失败、稳定成功四类，然后写入 skill 里一个受保护的 slow-update 区域。

## 5. 主要结果

SkillOpt 在六个 benchmark（SearchQA、SpreadsheetBench、OfficeQA、DocVQA、LiveMathematicianBench、ALFWorld）、七个目标模型、三种执行模式（direct chat、Codex、Claude Code）共 52 个评测格子上拿到全部最佳或并列最佳。

- GPT-5.5 Direct chat 平均提升 +23.5 分
- GPT-5.5 Codex 平均提升 +24.8 分
- GPT-5.5 Claude Code 平均提升 +19.1 分

SkillOpt 在每个 benchmark 上都超越了 Human skill、LLM skill、Trace2Skill、TextGrad、GEPA 和 EvoSkill 等基线方法。

## 6. 消融实验

消融实验验证了各组件的必要性：
- **文本学习率**：移除后性能下降，说明有界编辑防止破坏性重写
- **Rejected buffer**：移除后性能下降，说明失败编辑的反馈有价值
- **Update memory**：移除 meta skill 和 slow update 后性能显著下降
