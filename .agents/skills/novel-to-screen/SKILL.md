---
name: novel-to-screen
description: "Adapt novels into AI-generated screen works. Multi-agent pipeline: analysis → screenplay → visual design → storyboard with executable AI image/video prompts."
version: 0.1.0
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

将小说/文学作品改编为AI影视作品。多Agent协作，输出可执行的AI图片/视频生成提示词。

## 分类体系

三个维度组合：**制作手段·类型·体裁**

- **类型**：真人（写实）| 动画（2D/3D/水墨/赛璐璐/像素/绘本/混合）
- **体裁**：短剧 | 微电影 | 电影 | 电视剧

示例：`AI·动画(3D)·电影`、`AI·真人·短剧`

## 工作流

```
Phase 0: 项目初始化 → 确定分类、组建团队、设定风格约束
Phase 1: 原著分析 → novel-analyst → 原著分析报告
Phase 2: 剧本开发 → screenwriter（必须阅读原著+分析报告）→ 完整剧本
Phase 3: 视觉设计（并行）→ casting-director + scene-designer + costume-designer + action-director
Phase 4: 分镜整合 → director → 详细分镜剧本（含AI视频提示词）
Phase 5: 质量把控 → producer → 最终制作包
```

## 团队配置

按体裁自动配置，详见 `references/team-config.md`：

| 体裁 | 规模 | 兼职 |
|------|------|------|
| 短剧 | 5人 | 选角兼服化道、场景兼动作、导演兼制片 |
| 微电影 | 6人 | 场景兼服化道、导演兼制片 |
| 电影 | 8人 | 完整配置 |
| 电视剧 | 8-10人 | 完整+统筹 |

## Agent 职责速览

| Agent | 输出 | 提示词 |
|-------|------|--------|
| novel-analyst | 原著分析报告 | — |
| screenwriter | 完整剧本 | — |
| casting-director | 人物画像卡 | ✅ 图片提示词 |
| scene-designer | 场景设计 | ✅ 图片提示词 |
| costume-designer | 服化道方案 | ✅ 图片提示词 |
| action-director | 动作描述 | ✅ 视频提示词 |
| director | 分镜剧本 | ✅ 视频提示词（整合所有参考） |
| producer | 质量报告 | — |

## 提示词引用机制

导演的视频提示词通过引用上游图片生成结果整合：

```
镜头提示词 = 场景参考 + 人物参考 + 服化道参考 + 动作参考 + 运镜 + 时长
```

## 使用方式

1. 用户提供原著文本/文件 + 分类选择（类型+体裁+面风格）
2. 按 Phase 0-5 顺序执行，Phase 3 并行调度
3. 每个Phase完成后输出到项目目录，下一Phase读取上游输出
4. 最终输出：完整分镜剧本 + 所有AI生成提示词

## 目录结构

```
novel-to-screen/
├── SKILL.md                 # 本文件
├── agents/                  # 子Agent定义
│   ├── novel-analyst.md
│   ├── screenwriter.md
│   ├── casting-director.md
│   ├── scene-designer.md
│   ├── costume-designer.md
│   ├── action-director.md
│   ├── director.md
│   └── producer.md
├── references/
│   ├── genre_templates/     # 体裁模板
│   ├── style_presets/       # 面风格预设
│   └── prompt_guides/       # 提示词编写指南
└── scripts/                 # 工具脚本
```

## 待确认事项

- 提示词格式是否针对特定AI工具优化（Midjourney/Flux/Kling/Sora）
- Phase 3 并行阶段是否需要角色间中间同步
- 各角色蒸馏方向偏好（中国影视 vs 国际影视）
