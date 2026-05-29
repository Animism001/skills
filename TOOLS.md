# TOOLS.md - 技能索引

## 技能创建与蒸馏

| 技能 | 行数 | 用途 |
|------|------|------|
| skill-creator | 485 | 通用技能创建、评测、迭代 |
| huashu-nuwa | 644 | 从人名/主题蒸馏人物视角 Skill |
| dot-skill | 117 ✅ | 从同事/亲密关系/公众人物蒸馏 Skill（飞书/钉钉采集） |
| book2skill | — | 从书籍提炼可执行技能 |
| skillnet | 275 | 技能搜索、下载（search/download 免费，create/evaluate/analyze 由我直接做） |

## 技能管理与优化

| 技能 | 行数 | 用途 |
|------|------|------|
| skill-cleaner | 56 ✅ | 技能审计、Token 预算核算、描述精简 |
| self-improving | 250 | 分层记忆、自反思、自动衰减 |
| self-improving-agent | 644 | 日志驱动、晋升机制、技能提取 |
| clawhub | 151 | ClawHub 技能搜索、发现、安装 |
| find-skills | 142 | 技能发现与推荐 |

## 搜索与获取

| 技能 | 行数 | 用途 |
|------|------|------|
| anysearch | — | 实时搜索引擎（16引擎聚合） |
| multi-search-engine | 154 | 16引擎聚合搜索 |
| web-researcher | 21 ✅ | 深度研究、事实核查 |
| literature-search | 53 | 学术文献检索（Google Scholar/PubMed/arXiv等） |
| bilibili-search | 235 | B站视频搜索 |
| zlibrary | 134 | Z-Library 书籍搜索下载 |
| book-fetch | 46 | Anna's Archive 电子书下载 |
| weread-skills | 171 | 微信读书搜索/书架/笔记/书评/推荐 |

## 知识库与笔记

| 技能 | 行数 | 用途 |
|------|------|------|
| ima-skill | 285 | IMA 知识库+笔记管理（多模块） |

## 创作类

| 技能 | 行数 | 用途 |
|------|------|------|
| novel-to-screen | 78 | 小说AI影视化改编（多Agent协作，8角色流水线） |
| history-story | 235 | 历史故事创作（D.E.S.I.R.E.矩阵） |
| inkos | 46 | 长篇小说生成（多Agent流水线） |

## 文本人性化

| 技能 | 行数 | 语言 | 用途 |
|------|------|------|------|
| humanize-chinese | 242 | 中文 | 检测+改写AI中文，20+检测类别，7种风格转换，三大重写策略 |
| ai-humanizer | 149 | 英文 | 检测+改写AI英文，24模式检测器，500+AI词汇3层，统计分析 |

**适用规则**：仅对角色扮演类/创作类技能（需个性化输出）使用。工具类技能不需要去AI味。两层检测：①技能示例 ②生成内容。

## 路标化状态

✅ = 已路标化（≤80行），待改造：huashu-nuwa(644)、skill-creator(485)

## 目录

- 技能存放：`./.agents/skills/`
- PRD 存放：`./PRD/`
- 技能包存放：`./skillzip/`
- 参考文档：`./references/`
- 书籍资料：`./library/`
- 临时文件：`./temp/`
