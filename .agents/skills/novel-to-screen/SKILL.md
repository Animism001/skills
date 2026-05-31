---
name: novel-to-screen
description: "Adapt novels into AI-generated screen works. Multi-agent pipeline with strict 3A audit: fidelity + format + completeness. Zero fabrication, full traceability."
version: 0.2.0
metadata:
  openclaw:
    emoji: 🎬
    structure: sub-agent
    requires:
      env: []
      bins:
        - python3
---

# novel-to-screen

将小说/文学作品改编为AI影视作品。多Agent协作，严格3A审核机制，100%忠实原著，禁止任何编造。

## ⚠️ 核心原则：禁止编造

**铁律：所有输出必须忠实于原著，禁止任何形式的编造！**

- ❌ 禁止添加任何非原著内容
- ❌ 禁止删减原著内容
- ❌ 禁止修改原著文字
- ❌ 禁止原创任何内容（除非明确标注为"原创"）
- ✅ 必须逐字保留原著内容
- ✅ 必须追踪所有输入输出
- ✅ 必须通过3A审核才能继续

### 惩罚机制

1. **首次违规**：返回重做，黄色警告
2. **二次违规**：返回重做，橙色警告，记录审计日志
3. **三次违规**：暂停Agent，通知管理员，人工介入

## 分类体系

三个维度组合：**制作手段·类型·体裁**

- **类型**：真人（写实）| 动画（2D/3D/水墨/赛璐璐/像素/绘本/混合）
- **体裁**：短剧 | 微电影 | 电影 | 电视剧

示例：`AI·动画(3D)·电影`、`AI·真人·短剧`

## 3A审核机制

### 三个审核Agent

1. **fidelity-auditor（忠实度审核）**：逐字比对原著，确保100%忠实
2. **format-auditor（格式审核）**：验证JSON格式和结构完整性
3. **completeness-auditor（完整性审核）**：检测遗漏，确保99%+覆盖率

### 审核协调员

**auditor-coordinator** 负责：
- 并行调度3个审核Agent
- 汇总审核结果
- 判定是否通过
- 控制流程推进

### 决策规则

**必须3个审核全部PASS，才能进入下一环节**

```
执行Agent完成
    ↓
并行启动3A审核
    ↓
全部PASS → 进入下一环节
    ↓
有失败 → 返回重做（最多3次）
    ↓
3次失败 → 人工介入
```

## 工作流（带3A审核）

```
Phase 0: 项目初始化
  └→ auditor-coordinator 审核配置
      └→ 3A审核全部通过 → 下一阶段

Phase -1: 原文转JSON剧本
  └→ literature-to-json-script 执行
      └→ 记录输入输出哈希
          └→ auditor-coordinator 启动3A审核
              ├→ fidelity-auditor：逐字比对原著
              ├→ format-auditor：验证JSON结构
              └→ completeness-auditor：检测遗漏
                  └→ 3A全部PASS → 下一阶段

Phase 1: 原著分析
  └→ novel-analyst（阅读JSON剧本+原著）
      └→ 记录输入输出哈希
          └→ 3A审核全部通过 → 下一阶段

Phase 2: 剧本开发
  └→ screenwriter（阅读JSON剧本+分析报告+原著）
      └→ 记录输入输出哈希
          └→ 3A审核全部通过 → 下一阶段
  └→ 剧本朗读会

Phase 3: 视觉设计（并行）
  └→ casting-director、scene-designer、costume-designer、action-director
      └→ 各Agent独立执行和3A审核
          └→ 交叉讨论
              └→ 中期同步会
                  └→ 3A审核全部通过 → 下一阶段

Phase 4: 分镜整合
  └→ director（阅读JSON剧本+所有上游输出+原著）
      └→ 3A审核全部通过
          └→ 联合审稿会

Phase 5: 质量把控
  └→ producer（对照JSON剧本+原著检查）
      └→ 最终3A审核
          └→ 最终制作包
```

## 追踪机制

### 哈希链

每个环节的输出必须包含：
```json
{
  "metadata": {
    "source_file_hash": "原著SHA256哈希",
    "parent_hash": "上一环节输出哈希",
    "created_at": "ISO时间戳",
    "created_by": "Agent名称",
    "execution_id": "执行ID"
  }
}
```

### 审计日志

所有执行记录存储在 `audit/` 目录：
```
audit/
├── phase-0/
│   ├── config.json
│   ├── 3a-reports/
│   │   ├── fidelity-report.json
│   │   ├── format-report.json
│   │   └── completeness-report.json
│   └── coordinator-report.json
├── phase-1/
│   └── ...
└── hash-chain.json
```

## Agent 职责速览

### 执行Agent

| Agent | 输入 | 输出 | 3A审核 |
|-------|------|------|--------|
| literature-to-json-script | 原著文本 | JSON剧本 | ✅ |
| novel-analyst | JSON剧本+原著 | 分析报告 | ✅ |
| screenwriter | JSON剧本+报告+原著 | 完整剧本 | ✅ |
| casting-director | JSON剧本+剧本+原著 | 人物画像 | ✅ |
| scene-designer | JSON剧本+剧本+原著 | 场景设计 | ✅ |
| costume-designer | JSON剧本+剧本+画像+原著 | 服化道方案 | ✅ |
| action-director | JSON剧本+剧本+画像+原著 | 动作描述 | ✅ |
| director | JSON剧本+所有上游+原著 | 分镜剧本 | ✅ |
| producer | JSON剧本+所有上游+原著 | 质量报告 | ✅ |

### 审核Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| fidelity-auditor | 忠实度审核 | 逐字比对报告 |
| format-auditor | 格式审核 | 格式验证报告 |
| completeness-auditor | 完整性审核 | 覆盖率报告 |
| auditor-coordinator | 协调审核 | 汇总决策报告 |

## 团队配置

| 体裁 | 规模 | 兼职 |
|------|------|------|
| 短剧 | 8人 | 执行5+审核3 |
| 微电影 | 9人 | 执行6+审核3 |
| 电影 | 11人 | 执行8+审核3 |
| 电视剧 | 13人 | 执行10+审核3 |

## 使用方式

1. 用户提供原著文本/文件 + 分类选择（类型+体裁+面风格）
2. **必须使用pandoc或其他工具将原著转换为Markdown/TXT**
3. 按 Phase 0 → -1 → 1 → 2 → 3 → 4 → 5 顺序执行
4. **每个Phase必须通过3A审核才能继续**
5. 所有输出记录哈希到审计日志
6. 最终输出：完整分镜剧本 + 所有AI生成提示词 + 审计报告

## 目录结构

```
novel-to-screen/
├── SKILL.md                 # 本文件
├── agents/                  # 子Agent定义
│   ├── execution/           # 执行Agent
│   │   ├── literature-to-json-script.md
│   │   ├── novel-analyst.md
│   │   ├── screenwriter.md
│   │   ├── casting-director.md
│   │   ├── scene-designer.md
│   │   ├── costume-designer.md
│   │   ├── action-director.md
│   │   ├── director.md
│   │   └── producer.md
│   └── audit/              # 审核Agent
│       ├── fidelity-auditor.md
│       ├── format-auditor.md
│       ├── completeness-auditor.md
│       └── auditor-coordinator.md
├── references/
│   ├── execution/           # 执行Agent蒸馏资料
│   └── audit/              # 审核Agent蒸馏资料
├── scripts/                 # 工具脚本
└── audit/                  # 审计日志（执行时生成）
    ├── phase-0/
    ├── phase-1/
    └── hash-chain.json
```

## 审核报告要求

### fidelity-auditor 报告

```json
{
  "status": "PASS|FAIL",
  "checks": {
    "no_addition": "PASS|FAIL",
    "no_deletion": "PASS|FAIL",
    "no_modification": "PASS|FAIL",
    "character_names": "PASS|FAIL",
    "timeline": "PASS|FAIL"
  },
  "issues": [
    {
      "type": "addition|deletion|modification",
      "location": "位置",
      "original": "原著内容",
      "output": "输出内容",
      "severity": "critical|major|minor"
    }
  ]
}
```

### format-auditor 报告

```json
{
  "status": "PASS|FAIL",
  "checks": {
    "json_valid": "PASS|FAIL",
    "required_fields": "PASS|FAIL",
    "field_types": "PASS|FAIL",
    "hashes_present": "PASS|FAIL"
  },
  "issues": []
}
```

### completeness-auditor 报告

```json
{
  "status": "PASS|FAIL",
  "coverage": {
    "character_count_percentage": 99.5,
    "chapter_count_percentage": 100,
    "key_dialogues_percentage": 100
  },
  "issues": [
    {
      "type": "missing_content",
      "location": "位置",
      "original_content": "遗漏内容",
      "severity": "critical|major|minor"
    }
  ]
}
```

### auditor-coordinator 最终决策

```json
{
  "final_decision": "PASS|FAIL|RETRY",
  "retry_count": 0,
  "all_audits_passed": true|false,
  "next_action": "进入下一阶段|返回重做|人工介入"
}
```

## 待确认事项

- [ ] 提示词格式是否针对特定AI工具优化（Midjourney/Flux/Kling/Sora）
- [ ] 各角色蒸馏方向偏好（中国影视 vs 国际影视）
