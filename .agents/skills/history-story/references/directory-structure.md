# 目录结构

## 原始数据

```
./dayinhistory/                    # 原始历史事件数据
  {MM}/                            # 两位数月份（如 05）
    {DD}/                          # 两位数日期（如 22）
      events.md                    # 当日所有历史事件概览
      {event-slug}/                # 具体事件调研目录
        research.md                # 史实调研结果
```

## 创作素材与成品

```
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

## 命名规则

`{event-slug}` 命名规则：`{年份}-{事件简称}`，如 `192-董卓被诛`、`1945-广岛原子弹`。
