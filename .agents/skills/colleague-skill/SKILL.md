---
name: dot-skill
description: "Distill colleague, relationship, or celebrity characters into reusable Skills. Triggers on: 蒸馏同事, 蒸馏人物, 创建人物skill, colleague skill, relationship skill, celebrity skill, 名人skill, dot-skill. Supports Feishu/DingTalk auto-collection, dual-track analysis (Work + Persona), and evolution via file append & conversation correction."
argument-hint: "[character] [name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# dot-skill 创建器

统一 meta-skill 引擎，把 colleague、relationship、celebrity 三类对象蒸馏成可复用 Skill。

> 所有 Bash 命令在当前 SKILL.md 所在目录执行。`tools/...` 和 `prompts/...` 均为相对路径。

## 触发条件

- `/dot-skill`、"帮我创建一个 skill"、"我想蒸馏一个人"、"新建一个 skill"、"给我做一个 XX 的 skill"
- 进化模式："我有新文件"/"追加"、"这不对"/"他应该是"、`/update-skill {character} {slug}`

## Character Family

| Family | 对象 | intake | persona analyzer | persona builder | merger | storage root |
|--------|------|--------|-----------------|----------------|--------|-------------|
| colleague | 同事 | `prompts/intake.md` | `prompts/persona_analyzer.md` | `prompts/persona_builder.md` | `prompts/merger.md` | `./skills/colleague/{slug}` |
| relationship | 亲密关系 | `prompts/relationship/intake.md` | `prompts/relationship/persona_analyzer.md` | `prompts/relationship/persona_builder.md` | `prompts/relationship/merger.md` | `./skills/relationship/{slug}` |
| celebrity | 公众人物 | `prompts/celebrity/intake.md` | `prompts/celebrity/persona_analyzer.md` | `prompts/celebrity/persona_builder.md` | `prompts/celebrity/merger.md` | `./skills/celebrity/{slug}` |

共用：`prompts/work_analyzer.md` + `prompts/work_builder.md` + `prompts/correction_handler.md`

## 主流程：创建新 Skill

### Step 0：确认 character family

如果用户使用 `/dot-skill`，先确认类型：colleague / relationship / celebrity。
celebrity 需额外确认 research profile：budget-friendly（默认）/ budget-unfriendly（深度版）。

### Step 1：基础信息录入

读取对应 intake prompt，问 3 个问题：
1. **花名/代号**（必填）
2. **基本信息**（一句话：公司、职级、职位、性别）
3. **性格画像**（一句话：MBTI、星座、个性标签、印象）

除姓名外均可跳过。收集完后汇总确认。

### Step 2：原材料导入

5 种方式（可混用，可跳过）：

| 方式 | 说明 | 详情 |
|------|------|------|
| A 飞书自动采集 | 输入姓名，自动拉取消息+文档 | `references/data-collection.md` |
| B 钉钉自动采集 | 输入姓名，自动拉取文档 | `references/data-collection.md` |
| C 飞书链接 | 文档/Wiki 链接 | `references/data-collection.md` |
| D 上传文件 | PDF/图片/JSON/邮件 | `references/data-collection.md` |
| E 直接粘贴 | 复制文字 | 无需工具 |

详细采集流程和 API 调用方式见 `references/data-collection.md`。

### Step 3：分析原材料

celebrity 需先走 research 子流程，详见 `references/celebrity-flow.md`。

双线路并行分析：

**线路 A（Work Skill）**：参考 `prompts/work_analyzer.md`
- 提取：负责系统、技术规范、工作流程、输出偏好、经验知识
- celebrity 场景下 work 偏方法论、判断框架、决策习惯

**线路 B（Persona）**：使用对应 family 的 persona analyzer
- 将用户标签翻译为具体行为规则
- 提取：表达风格、决策模式、人际行为
- celebrity 必须保留：mental models / decision heuristics / expression DNA / contradictions / honest boundaries

### Step 4：生成并预览

- Work：`prompts/work_builder.md`
- Persona：对应 family 的 persona builder（celebrity + budget-unfriendly 用 `prompts/celebrity/budget_unfriendly/persona_builder.md`）
- 展示摘要（各 5-8 行），询问确认

### Step 5：写入文件

1. 解析 storage root
2. `Write` 三个临时文件：`/tmp/dot_skill_{slug}_meta.json` + `_work.md` + `_persona.md`
3. 调用：
   ```bash
   python3 tools/skill_writer.py \
     --action create \
     --character {character} \
     --research-profile {research_profile} \
     --slug {slug} \
     --name "{name}" \
     --meta /tmp/dot_skill_{slug}_meta.json \
     --work /tmp/dot_skill_{slug}_work.md \
     --persona /tmp/dot_skill_{slug}_persona.md \
     --base-dir {resolved_base_dir}
   ```
4. celebrity 创建后执行 quality check：
   ```bash
   python3 tools/research/quality_check.py "{base_dir}/{slug}/SKILL.md" --profile {research_profile}
   ```

## 进化模式

详见 `references/evolution-guide.md`：
- **追加文件**：merger 分析增量 → skill_writer.py update
- **对话纠正**：correction_handler 识别 → Work/Persona 分类 → skill_writer.py update

## Reference Files

| Need | File |
|------|------|
| 数据采集详细流程（飞书/钉钉/链接/文件） | `references/data-collection.md` |
| Celebrity 蒸馏流程（budget-friendly/unfriendly） | `references/celebrity-flow.md` |
| 进化模式详细指南 | `references/evolution-guide.md` |
| English version of this SKILL.md | `references/skill-en.md` |
