# Nuwa 技能强化 Workflow 设计

## 📋 目录结构

```
/workspace/
├── skills/                          # 用户技能目录
│   └── robert-mckee-perspective/    # 示例人物技能
└── tools/                           # 工具技能目录
    ├── huashu-nuwa/                  # 女娲核心技能
    ├── skill-creator/                 # 技能创建工具
    ├── multi-search-engine/           # 多引擎搜索 ⭐
    ├── web-researcher/                # 网络深度调研
    ├── zlibrary/                      # Z-Library 书籍获取
    ├── literature-search/             # 学术文献搜索
    ├── book-fetch/                    # 电子书获取（Anna's Archive）
    ├── bilibili-search/               # B站 视频搜索
    ├── bilibili-transcript/           # B站 字幕获取
    ├── youtube-transcript/            # YouTube 字幕获取
    └── thinking-model-enhancer/       # 思维模型增强
```

---

## 🎯 Nuwa 各阶段强化方案

### Phase 0: 需求分析与分流

**现有流程**：
- 明确人名 → 直接路径
- 模糊需求 → 诊断路径 → 推荐候选

**强化方案**：
- 保持现有流程不变
- *增强*：使用 `thinking-model-enhancer` 辅助需求诊断

---

### Phase 1: 多源信息采集（6个并行Agent）⭐ 重点强化

#### Agent 1: 著作调研
**目标**：书籍、长文、论文、newsletter

**强化 Workflow**：
```
1. multi-search-engine → 搜索相关书籍/文章（16个引擎）
   → 中文：百度/Bing CN/360/搜狗/微信搜索/神马
   → 英文：Google/Google HK/DuckDuckGo/Yahoo/Startpage/Brave

2. （可选）zlibrary → 搜索并下载电子书
   → 优先使用用户提供的本地素材

3. （可选）literature-search → 搜索学术文献
   → Google Scholar/PubMed/arXiv/IEEE/ACM等

4. （可选）web-researcher → 深度调研长文
```

**输出文件**：`references/research/01-writings.md`

---

#### Agent 2: 对话调研
**目标**：播客、长视频、AMA、深度采访

**强化 Workflow**：
```
1. multi-search-engine → 搜索相关视频/播客
   → 中文：百度搜索 + site:bilibili.com
   → 英文：Google/Google HK + site:youtube.com

2. （可选）bilibili-search → 搜索 B站 视频
   → 输入关键词 → 获取视频列表（含 BV号、标题、UP主、播放量）

3. （可选）bilibili-transcript → 获取字幕
   → 提供 BV号 → 下载字幕（CC/AI/Whisper）

4. （可选）youtube-transcript → 获取字幕
   → 提供视频链接 → 下载字幕
```

**输出文件**：`references/research/02-conversations.md`

---

#### Agent 3: 表达风格调研
**目标**：Twitter/X、微博、即刻、短文

**强化 Workflow**：
```
1. multi-search-engine → 搜索社交媒体内容
   → 中文：百度/搜狗/微信搜索 + site:weibo.com
   → 英文：Google/DuckDuckGo + site:twitter.com

2. （可选）web-researcher → 深度分析表达模式
   → 高频用词、句式偏好、幽默方式等
```

**输出文件**：`references/research/03-expression-dna.md`

---

#### Agent 4: 他者视角调研
**目标**：他人分析、书评、批评、传记

**强化 Workflow**：
```
1. multi-search-engine → 搜索他人评价
   → 中文：百度/Bing CN/360
   → 英文：Google/Google HK/DuckDuckGo

2. （可选）web-researcher → 深度分析外部观点
   → 争议点、批评、与同行对比
```

**输出文件**：`references/research/04-external-views.md`

---

#### Agent 5: 决策调研
**目标**：重大决策、转折点、争议行为

**强化 Workflow**：
```
1. multi-search-engine → 搜索决策相关信息
   → 新闻报道、访谈记录、内部文档

2. （可选）web-researcher → 深度分析决策逻辑
   → 决策背景、事后反思、言行一致案例
```

**输出文件**：`references/research/05-decisions.md`

---

#### Agent 6: 时间线调研
**目标**：出生/出道到现在的完整时间线

**强化 Workflow**：
```
1. multi-search-engine → 搜索时间线信息
   → 关键里程碑、思想转折点
   → 特别注意：最近12个月动态（防过时）

2. （可选）web-researcher → 整理时间线
```

**输出文件**：`references/research/06-timeline.md`

---

### Phase 1.5: 调研质量检查

**强化方案**：
- 使用 `merge_research.py` 生成摘要表格
- *增强*：使用 `thinking-model-enhancer` 初步评估信息质量

---

### Phase 2: 思维框架提炼 ⭐ 重点强化

**现有流程**：
- 心智模型提取（3-7个）
- 决策启发式提取（5-10条）
- 表达DNA分析
- 价值观与反模式
- 诚实边界

**强化方案**：
```
1. 读取 extraction-framework.md（三重验证方法论）

2. 使用 thinking-model-enhancer 增强提炼
   → 辅助心智模型验证（跨域复现/生成力/排他性）
   → 优化表达DNA分析
   → 识别内在张力和矛盾

3. （可选）web-researcher → 补充交叉验证
```

---

### Phase 3-4: Skill构建与质量验证

**强化方案**：
- 使用 `skill-creator` 辅助构建标准化 Skill
- 使用 `quality_check.py` 进行质量验证
- *增强*：使用 `thinking-model-enhancer` 优化 Skill 内容

---

### Phase 5: 双Agent精炼

**强化方案**：
- 使用 `thinking-model-enhancer` 作为 Agent A（优化视角）
- 使用 `skill-creator` 作为 Agent B（Skill 构建视角）

---

## 🔧 技能调用优先级

### Phase 1 信息采集优先级

| 维度 | 首选技能 | 次选技能 | 备选技能 |
|------|---------|---------|---------|
| **通用搜索** | multi-search-engine | web-researcher | — |
| **书籍获取** | zlibrary | book-fetch | literature-search |
| **文献搜索** | literature-search | multi-search-engine | — |
| **B站视频** | bilibili-search | multi-search-engine | — |
| **B站字幕** | bilibili-transcript | — | — |
| **YouTube字幕** | youtube-transcript | — | — |

### Phase 2 框架提炼优先级

| 任务 | 首选技能 | 次选技能 |
|------|---------|---------|
| **心智模型验证** | thinking-model-enhancer | extraction-framework.md |
| **表达DNA优化** | thinking-model-enhancer | — |

### Phase 3-5 Skill构建

| 任务 | 首选技能 | 次选技能 |
|------|---------|---------|
| **Skill构建** | skill-creator | skill-template.md |
| **质量验证** | quality_check.py | thinking-model-enhancer |

---

## 📊 完整工作流图

```
用户输入
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 0: 需求分析与分流            │
│ - 明确人名 → 直接路径              │
│ - 模糊需求 → 诊断路径              │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 0.5: 创建Skill目录           │
└─────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────────┐
│ Phase 1: 6个并行Agent深度调研                          │
│                                                          │
│  Agent 1: 著作          │  Agent 2: 对话              │
│  ├─ multi-search-engine │  ├─ multi-search-engine    │
│  ├─ zlibrary           │  ├─ bilibili-search       │
│  ├─ literature-search  │  └─ bilibili-transcript   │
│  └─ web-researcher     │  └─ youtube-transcript    │
│                                                          │
│  Agent 3: 表达          │  Agent 4: 他者              │
│  ├─ multi-search-engine │  └─ multi-search-engine    │
│  └─ web-researcher     │  └─ web-researcher        │
│                                                          │
│  Agent 5: 决策          │  Agent 6: 时间线            │
│  ├─ multi-search-engine │  └─ multi-search-engine    │
│  └─ web-researcher     │                             │
└───────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 1.5: 调研质量检查            │
│ - merge_research.py                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 2: 思维框架提炼               │
│ - extraction-framework.md           │
│ - thinking-model-enhancer ⭐        │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 3: Skill构建                  │
│ - skill-creator ⭐                  │
│ - skill-template.md                 │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 4: 质量验证                   │
│ - quality_check.py                  │
│ - thinking-model-enhancer           │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Phase 5: 双Agent精炼               │
│ - thinking-model-enhancer (Agent A)│
│ - skill-creator (Agent B)          │
└─────────────────────────────────────┘
    │
    ▼
完成！交付 Skill
```

---

## 🎯 使用示例

### 示例 1: 蒸馏 Elon Musk

```
1. Phase 0: 明确人名 → 直接路径
2. Phase 1:
   - Agent 1: multi-search-engine + zlibrary
   - Agent 2: multi-search-engine (YouTube) + youtube-transcript
   - Agent 3-6: multi-search-engine + web-researcher
3. Phase 2: thinking-model-enhancer 辅助提炼
4. Phase 3-5: skill-creator + quality_check.py
```

### 示例 2: 蒸馏中国人物（如张一鸣）

```
1. Phase 0: 明确人名 → 直接路径
2. Phase 1:
   - Agent 1: multi-search-engine (国内引擎) + zlibrary
   - Agent 2: bilibili-search + bilibili-transcript
   - Agent 3-6: multi-search-engine (百度/搜狗/微信搜索)
3. Phase 2-5: 同上
```

### 示例 3: 模糊需求（"我想提升决策质量"）

```
1. Phase 0: 模糊需求 → 诊断路径
   - 使用 thinking-model-enhancer 辅助诊断
2. Phase 0B: 推荐候选（芒格/塔勒布/纳瓦尔）
3. 用户选择后 → 进入 Phase 1-5
```

---

## ⚠️ 注意事项

1. **multi-search-engine 是核心**：16个引擎覆盖国内外，优先使用
2. **尊重用户提供的本地素材**：优先级 > 网络搜索
3. **中国人物 vs 西方人物**：自动切换搜索引擎策略
4. **信息源黑名单**：知乎、微信公众号、百度百科始终排除
5. **Cookie 管理**：multi-search-engine 的 Cookie 仅存内存，不持久化
6. **速率限制**：multi-search-engine 自动 1-2 秒延迟，尊重服务器

---

## 📚 参考文档

- [huashu-nuwa/SKILL.md](file:///workspace/skills/huashu-nuwa/SKILL.md) - 女娲核心技能
- [huashu-nuwa/references/extraction-framework.md](file:///workspace/skills/huashu-nuwa/references/extraction-framework.md) - 思维框架提炼方法论
- [multi-search-engine/SKILL.md](file:///workspace/skills/multi-search-engine/SKILL.md) - 多引擎搜索技能
- [skill-creator/SKILL.md](file:///workspace/skills/skill-creator/SKILL.md) - 技能创建工具
- [thinking-model-enhancer/SKILL.md](file:///workspace/skills/thinking-model-enhancer/SKILL.md) - 思维模型增强
