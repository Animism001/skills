# 影视选角导演方法论蒸馏

## 一、核心心智模型（5个）

### 心智模型1：角色锚定模型（Character Anchor）

**核心逻辑**：选角的第一步不是"找演员"，而是"锚定角色"。角色锚定是从剧本文字到视觉画像的翻译过程，输出物是角色拆解文档（Character Breakdown）。

**操作框架**：
1. **角色传记**：完整背景故事、动机、弧线
2. **关系动力学**：与其他角色的关系图谱和张力结构
3. **情感范围**：角色需要覆盖的情绪光谱和复杂度
4. **外在要求**：年龄范围、外貌特征、身体条件及灵活度
5. **特殊技能**：武术、歌唱、骑术、方言等硬性要求
6. **视觉气质**：角色给观众的第一印象关键词（3-5个）

**来源**：Feature Film Casting Process, C-I Studios（c-istudios.com）；The Casting Handbook, Catliff & Granville, Routledge（routledge.com）；ScreenSkills Casting Director Job Profile（screenskills.com）

---

### 心智模型2：化学矩阵模型（Chemistry Matrix）

**核心逻辑**：选角不是对单个角色的独立决策，而是对角色之间化学反应的系统性设计。每个选角决策都影响整体群像的生态平衡。

**操作框架**：
1. **互补性原则**：主角团内部性格/气质必须互补，避免"技能撞车"（如两个话痨搞笑角色会稀释叙事焦点）
2. **张力结构**：正派与反派之间需要能力对等但价值观冲突
3. **反差选角**：演员本人性格与角色形成反差时，往往产生意外惊喜（如《陈情令》中宣璐本人开朗却演温柔师姐、汪卓成外表温和却演暴躁江澄）
4. **化学测试**：对主角配对进行试戏，观察对话节奏、肢体舒适度、情感真实性
5. **群像闭环**：整个卡司构成一个自洽的微型社会，每个角色承担独特功能

**来源**：《陈情令》反差选角揭秘（sina.cn）；Feature Film Casting Process, Chemistry Testing章节（c-istudios.com）；《满江红》选角美学分析

---

### 心智模型3：形神互译模型（Form-Spirit Translation）

**核心逻辑**：外在形象（形）与内在性格（神）之间是双向翻译关系——形可传神，神可塑形。选角/角色设计的核心难题是让两者互为表达、互相强化。

**操作框架**：
1. **从神到形**：先定义角色性格内核，再推导外在特征
   - 性格关键词→形状语言（圆形=友善、方形=稳重、三角形=危险）
   - 性格关键词→色彩系统（暖色=热情/正义、冷色=疏离/阴暗）
   - 性格关键词→体态特征（阳刚多用直线、阴柔多用曲线）
2. **从形到神**：先确定视觉锚点，再反向丰富性格层次
   - 特定外貌特征（如伤疤、异色瞳）→推导角色经历
   - 服装细节（破损战甲→久经沙场、精致配饰→身份地位）
3. **形神统一验证**：角色设计完成后，用"换人测试"检验——"换别的都不成立"才算成功

**来源**：《哪吒》角色设计师申威访谈（sina.com.cn, gdzjdaily.com.cn）；追光动画角色设计方法论（《现代电影技术》）；Character Design Concept Art Guide（incredimate.com）；迪士尼Visual Development流程（disneyanimation.com）

---

### 心智模型4：分层一致性模型（Layered Consistency）

**核心逻辑**：角色视觉表达需要在多个层级上保持一致性——从宏观的气质调性到微观的皮肤纹理，每一层都有不同的锁定策略和容错范围。

**操作框架**（从宏观到微观）：
1. **气质层**（最稳定）：角色的整体感觉和辨识度，通过性格关键词+核心slogan锁定
2. **轮廓层**：角色的剪影辨识度，通过正面+侧面黑影测试验证
3. **色彩层**：6-8色配色系统，建立角色视觉身份证
4. **结构层**：面部骨骼、体型比例、五官特征，通过多角度视图锁定
5. **纹理层**（最易漂移）：皮肤质感、服装材质、毛发细节，需要反复校准

**AI生成中的对应策略**：
- 气质层：提示词中固定风格锚点（如"写实3D渲染，东方武侠风格"）
- 轮廓层：角色说明书（Character Sheet）+ 剪影测试
- 色彩层：色谱系统 + 色彩关键词
- 结构层：--cref角色参考 + --cw权重控制（Midjourney）/ 角色锚点图（GPT Image）
- 纹理层：quality设置 + 迭代修正

**来源**：Midjourney V7 Character Sheet Guide（selfielab.me）；优设网角色说明书方法论（uisdc.com）；OpenAI GPT Image Prompting Guide（developers.openai.com）；Consistent Characters in Midjourney（qwe.edu.pl）

---

### 心智模型5：文化适配模型（Cultural Adaptation）

**核心逻辑**：选角和角色设计必须嵌入特定的文化语境。不同文化对"美""丑""英雄""反派"的视觉编码不同，中国影视选角有独特的传统和审美逻辑。

**操作框架**：
1. **文化符号提取**：从传统文化中提取视觉符号
   - 《哪吒2》龙王设计参考故宫龙纹样、金木水火土五行色彩
   - 《长安三万里》人物造型参考唐俑、服饰参照唐画纹饰
   - 结界兽造型借鉴三星堆文物
2. **中式审美转译**：
   - 造型偏东方、线条偏圆润流畅
   - 配色灵感来自国画（淡雅、低饱和度）
   - 服饰褶皱运用雕刻手法
3. **"丑"的文化辩证**：
   - 中国动画角色的"丑"不是缺陷，而是性格放大器
   - 申威："丑只是把角色特点进行放大，加深观众感受"
   - 饺子："宁愿丑到没一个人喜欢，也不要普通到没一个人能记住"
4. **行业生态适配**：
   - 中国选角行业从"演员副导演"向"选角导演/Casting Director"转型
   - 选角公司梯队化运作（阵容导演→演员统筹→演员副导演→考察期成员）
   - 选角导演话语权有限，需与导演、制片人、资方、平台多方博弈

**来源**：《哪吒2》申威访谈（gdzjdaily.com.cn）；《长安三万里》技术实践（《现代电影技术》）；选角行业调查（huxiu.com, centrechina.com）；百度百科"选角导演"

---

## 二、决策启发式（8条）

### 启发式1：先拆解，后选角

在做任何选角/角色设计决策前，先完成角色拆解文档（Breakdown）。拆解决策先于选角决策。没有拆解的选角是盲目的。

> 来源：The Casting Handbook, "The Breakdown"章节；ScreenSkills Casting Director Profile

### 启发式2：剪影即身份

如果角色的纯黑剪影无法被辨认，设计就不成立。先做剪影测试，再细化。这是迪士尼角色设计的金标准，也适用于AI角色一致性验证。

> 来源：Character Design Concept Art Guide（incredimate.com）；优设网角色说明书方法论（uisdc.com）

### 启发式3：反差产生记忆点

演员本人与角色的反差、角色外貌与性格的反差，是制造记忆点的利器。但反差必须有内在逻辑支撑，不能为反差而反差。

> 来源：《陈情令》反差选角案例（sina.cn）；申威"美丑辩证"（sina.com.cn）

### 启发式4：每个角色只承载一个核心执念

角色设计时，给每个角色一个"执念"——一种极致的特质。中庸的角色会被观众过滤掉。功能重叠的角色会稀释叙事焦点。

> 来源：《满江红》选角美学分析

### 启发式5：AI生成角色时，锚点图比提示词更重要

用AI生成角色视觉时，先生成一张高质量的"锚点图"（正面、平光、纯色背景、中性表情），再以此为基础扩展。锚点图的质量决定后续所有生成的一致性上限。

> 来源：Midjourney --cref方法论（qwe.edu.pl）；OpenAI Character Anchor工作流（developers.openai.com）

### 启发式6：提示词结构遵循"场景→主体→细节→约束"

AI人物图像提示词的最佳结构：先设定场景/背景，再描述主体人物，再添加关键细节，最后声明约束条件（排除项、保持项）。用短句和逗号分隔，避免长段落。

> 来源：OpenAI GPT Image Prompting Guide（developers.openai.com）；Let's Enhance AI Prompt Guide（letsenhance.io）

### 启发式7：真人选角看"化学反应"，动画选角看"形神统一"

真人影视的选角核心是演员之间的化学反应（Chemistry Read），因为真人演员自带不可控的个人特质；动画角色设计的核心是形神统一，因为一切外在特征都是主动设计的结果。两者方法论不可混用。

> 来源：Feature Film Casting Process, Chemistry Testing（c-istudios.com）；《哪吒》申威访谈（sina.com.cn）；动画角色演技分析（知乎）

### 启发式8：迭代优于一次到位

无论是选角试镜还是AI角色生成，都采用"快速迭代"策略：先出粗版（self-tape/低质量生成），筛选后逐步精化（in-person callback/高质量生成+局部修正）。不要试图一步到位。

> 来源：Feature Film Casting Process, Audition Pipeline（c-istudios.com）；Midjourney Vary Region迭代法（qwe.edu.pl）；OpenAI "iterate instead of overloading"原则（developers.openai.com）

---

## 三、选角导演工作流程框架

### 阶段1：剧本拆解与角色定义

| 步骤 | 输出物 | 关键方法 |
|------|--------|---------|
| 剧本精读 | 角色清单 | 逐场标注角色出场与功能 |
| 角色拆解 | Character Breakdown文档 | 角色锚定模型6要素 |
| 视觉画像 | 角色视觉参考板（Moodboard） | 形神互译模型，从神到形 |
| 预算对齐 | 演员预算分配方案 | 按角色重要性分级预算 |

> 来源：The Casting Handbook；ScreenSkills；C-I Studios

### 阶段2：候选人搜索与筛选

| 步骤 | 方法 | 关键考量 |
|------|------|---------|
| 建立选角名单 | 每个主要角色研究15-20名演员，分三梯队 | 梯队1:明星/知名演员；梯队2:成熟性格演员；梯队3:新锐/特色演员 |
| Self-tape初筛 | 远程提交试镜视频 | 评估：角色适配度、独特性、技术能力、情感表达 |
| 比较矩阵 | 候选人优劣势对比表 | 记录：特殊技能、档期、经纪信息、备选排序 |

> 来源：C-I Studios Feature Film Casting Process

### 阶段3：深度试镜与化学测试

| 步骤 | 方法 | 关键考量 |
|------|------|---------|
| 现场试镜 | 冷读+准备独白+导演调整 | 评估：表演弹性、导演反馈接受度、个性匹配 |
| 化学测试 | 主角配对试戏 | 评估：对话节奏、肢体舒适度、情感真实性 |
| 试镜记录 | 标准化评估档案 | 科学完善的价值评估体系 |

> 来源：C-I Studios；网易"选角适配"文章（163.com）

### 阶段4：决策与锁定

| 步骤 | 方法 | 关键考量 |
|------|------|---------|
| 多方协商 | 导演+制片人+资方+平台圆桌 | 选角导演提供建议，无最终决定权 |
| 合同谈判 | 经纪公司对接 | 片酬、档期、署名、排他条款 |
| 备选方案 | 维护二级选角名单 | 应对演员退出、档期冲突 |

> 来源：选角行业调查（huxiu.com, centrechina.com）

---

## 四、角色视觉画像设计框架

### 4.1 角色说明书（Character Sheet）标准结构

基于优设网方法论和迪士尼/追光动画实践，提炼11模块标准结构：

| 模块 | 内容 | 面积权重 | AI生成要点 |
|------|------|---------|-----------|
| 1.身份卡 | 代号/职业/年龄/性格标签/核心slogan | 5% | 固定风格锚点 |
| 2.色谱系统 | 6-8色色标 | 3% | 色彩关键词 |
| 3.主形象展示 | 正/3-4侧/侧/背四视图，标准站姿 | 30%（最大） | --cref锚点图，--cw 70-80 |
| 4.轮廓剪影 | 正面+侧面纯黑剪影 | 5% | 纯色背景，纯黑填充 |
| 5.情绪矩阵 | 8种标准表情 | 15% | 固定角度/打光/服装，仅变表情 |
| 6.微表情 | 5种细节表情 | 8% | 眼睑/嘴角/下颌局部特写 |
| 7.头部结构 | 多角度头部 | 8% | 3-4侧/正侧/仰/俯 |
| 8.体态语汇 | 3种身体语言（松弛/戒备/笃定） | 8% | 肩膀/脊柱/腿部变化 |
| 9.情绪近景 | 1张强情绪胸像 | 5% | 高浓度情绪输出 |
| 10.服饰拆解 | 发式/面料/配件/足履4格 | 8% | 材质关键词 |
| 11.手势语汇 | 5种手势 | 5% | 松弛/紧绷/指示/握持/触面 |

> 来源：优设网角色说明书方法论（uisdc.com）；迪士尼Visual Development（disneyanimation.com）；Midjourney V7 Character Sheet Guide（selfielab.me）

### 4.2 AI人物图像提示词模板

#### 真人影视风格

```
[场景/背景], [年龄] [性别] [族群], [发型描述], [关键面部特征], [体型描述], [服装描述], [光影模式], [情绪/姿态], [镜头语言], [画质约束]

示例：
dimly lit traditional Chinese courtyard, 35-year-old Chinese woman, black hair in low bun with jade pin, sharp cheekbones with subtle scar on left brow, slender build, dark blue silk qipao with embroidered cranes, Rembrandt lighting from 45° side, guarded expression with slight tension in jaw, 85mm portrait lens, shallow depth of field, photorealistic, film grain, accurate white balance
```

#### 动画/概念设计风格

```
[风格锚点], character sheet of [角色描述], [四视图], [色彩系统], [情绪关键词], [文化参考], [材质约束], [版式约束]

示例：
stylized 3D render, Chinese mythological style, character sheet of a dragon king warrior, front/3-4/side/back views, white and pale blue-green palette with gold accents, regal and menacing, inspired by Ming dynasty dragon motifs and故宫纹样, metallic armor with scale texture, clean white background, 4:3 horizontal layout
```

> 来源：OpenAI GPT Image Prompting Guide（developers.openai.com）；Midjourney Portrait Prompts 2025（skywork.ai）；优设网（uisdc.com）

### 4.3 AI角色一致性保障策略

| 策略 | 适用工具 | 操作方法 |
|------|---------|---------|
| 角色锚点图 | 通用 | 先生成正面平光纯色背景锚点图，后续所有生成都引用此图 |
| --cref参考 | Midjourney | 使用锚点图URL，--cw 70-80控制一致性权重 |
| 种子值锁定 | Midjourney/SD | 使用--seed固定随机种子，减少变异 |
| 迭代修正 | 通用 | 生成→选择最佳→局部修正（Vary Region）→再生成 |
| 约束重申 | GPT Image | 每次迭代都重新声明"保持面部/比例/服装不变" |
| 负面提示 | SDXL | "plastic skin, waxy, over-smoothed, harsh color cast" |

> 来源：Midjourney --cref方法论（qwe.edu.pl, selfielab.me）；OpenAI Prompting Guide（developers.openai.com）；SDXL Portrait Guide（skywork.ai）

---

## 五、真人 vs 动画选角差异对照

| 维度 | 真人影视 | 动画/概念设计 |
|------|---------|-------------|
| 核心决策 | 演员选择（从已有池中匹配） | 角色创造（从零设计） |
| 外在可控性 | 低（演员自带外貌） | 高（一切外在特征主动设计） |
| 一致性挑战 | 演员跨场景表演一致性 | 角色360°视觉一致性 |
| 化学反应 | 演员间真实互动（Chemistry Read） | 角色间设计互补（关系力学设计） |
| 声音维度 | 演员自带声音 | 声优独立选配，声音与形象分离 |
| 迭代成本 | 高（重新试镜/换角成本大） | 低（修改设计稿/重新生成） |
| 文化适配 | 演员自带文化身份 | 需主动嵌入文化符号 |
| AI辅助方向 | 候选人视觉匹配、角色概念图 | 角色说明书生成、一致性维护 |

> 来源：动画角色演技分析（知乎）；《BEASTARS》3DCG角色塑造（gcores.com）；追光动画技术实践（《现代电影技术》）

---

## 六、中国影视选角行业特征

### 6.1 发展脉络

| 阶段 | 时期 | 特征 |
|------|------|------|
| 导演中心制 | 2008年以前 | 导演/资方绝对选角权，选角导演仅负责群演 |
| 行业觉醒 | 2009-2013 | "中国演员副导演协会"成立（400+人）；牧星人等首批工作室出现 |
| 公司化转型 | 2014-2019 | 浩瀚星盘、CD HOME、同人星光等头部公司化；梯队化运作 |
| 洗牌与拓展 | 2020至今 | 行业洗牌淘汰小团队；头部向经纪/制作拓展；平台话语权增强 |

### 6.2 行业特点

1. **关系驱动**：选角行业本质是"看人情的行业"，合作顺延性基于人际关系
2. **话语权有限**：选角导演提供建议，最终决定权在导演/制片人/资方/平台
3. **利润微薄**：项目选角团队费用5-10万/月，不随项目爆款增长
4. **梯队培养**：阵容导演→演员统筹→演员副导演→考察期成员，打怪升级模式
5. **多方博弈**：出品方、平台、导演、制片人都要参与选角决策

### 6.3 与好莱坞差异

| 维度 | 中国 | 好莱坞 |
|------|------|--------|
| 选角导演地位 | 建议者，"帮忙找人的" | 早期参与创作，可影响艺术风格 |
| 决策权 | 导演/资方/平台多方决策 | 选角导演有更大话语权 |
| 行业规范 | 仍在规范化过程中 | 成熟工业体系，有奥斯卡选角奖 |
| 代表案例 | 浩瀚星盘、CD HOME | Sarah Finn（漫威系列） |

> 来源：选角行业调查（huxiu.com, centrechina.com, cm3721.com）；36氪选角行业报道（36kr.com）

---

## 七、参考来源索引

1. C-I Studios - Feature Film Casting Process: https://c-istudios.com/feature-film-casting-process-professional-strategies-from-casting-directors/
2. ScreenSkills - Casting Director Job Profile: https://www.screenskills.com/job-profiles/browse/film-and-tv-drama/development-film-and-tv-drama-job-profiles/casting-director/
3. The Casting Handbook (Catliff & Granville, Routledge): https://www.routledge.com/The-Casting-Handbook-For-Film-and-Theatre-Makers/Catliff-Granville/p/book/9780415688246
4. Cineverse Magazine - Mastering the Casting Process: https://www.cineversemagazine.com/mastering-the-casting-process-in-contemporary-cinema-a-comprehensive-guide/
5. 迪士尼Visual Development: https://disneyanimation.com/process/visual-development/
6. Character Design Concept Art Guide (Incredimate): https://www.incredimate.com/blog/character-design-concept-art-complete-guide-for-beginners-and-professionals/
7. CGSpectrum - What is Character Design: https://www.cgspectrum.com/blog/what-is-character-design
8. Visual Arts Passage - Principles of Character Design: https://visualartspassage.com/blog/principles-of-character-design/
9. 《哪吒》角色设计师申威访谈: https://news.sina.com.cn/c/2019-08-19/doc-ihytcitn0381974.shtml
10. 《哪吒2》申威访谈: https://www.gdzjdaily.com.cn/p/2910926.html
11. 追光动画技术实践（《现代电影技术》）: https://c.m.163.com/news/a/JI5BMAM50517D0O2.html
12. 《陈情令》反差选角: https://ent.sina.cn/2026-05-27/detail-inhzikrs0863154.d.html
13. 选角行业调查（虎嗅）: https://m.huxiu.com/article/809282.html
14. 选角公司化（焦点中国）: https://www.centrechina.com/news/jiaodian/106815.html
15. 选角行业揭秘（传媒头条）: http://www.cm3721.com/m/view.php?aid=8740
16. 36氪选角报道: https://36kr.com/p/1641976430593
17. 优设网角色说明书方法论: https://www.uisdc.com/ai-character-blueprint
18. Midjourney V7 Character Sheet Guide: https://selfielab.me/blog/midjourney-v7-character-sheet-prompts-full-guide-20260223
19. Consistent Characters in Midjourney (QWE): https://www.qwe.edu.pl/tutorial/consistent-characters-midjourney/
20. OpenAI GPT Image Prompting Guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
21. Portrait Prompts 2025 (Skywork): https://skywork.ai/blog/how-to-portrait-prompts-2025/
22. Midjourney Character Reference Docs: https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference
23. Let's Enhance AI Prompt Guide: https://letsenhance.io/blog/article/ai-text-prompt-guide/
24. 《BEASTARS》3DCG角色塑造: https://www.gcores.com/articles/117446
25. 《恋与深空》GDC角色设计分享: https://www.cgames.com/contents/2/10717.html
26. Nano Banana角色拆解提示词: https://www.curify-ai.com/zh/nano-template/character
27. 知乎"影视剧是如何选角的": https://www.zhihu.com/question/39369452
28. 网易"选角适配有多重要": https://www.163.com/dy/article/I4VGE92N0517JF3D.html
29. 选角指导（台湾美感教育）: https://aade.project.edu.tw/annetimes/journal/22/
30. 百度百科"选角导演": http://baike.baidu.com/item/选角导演/5171316
