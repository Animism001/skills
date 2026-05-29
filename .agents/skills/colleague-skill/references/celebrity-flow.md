# Celebrity 蒸馏流程

## budget-friendly（默认）

1. 读取 `prompts/celebrity/research.md`，按 6 维度并行采集策略做 research planning
2. 创建目录：`mkdir -p "{skill_dir}/knowledge/research/raw" "{skill_dir}/knowledge/research/merged"`
3. 确认采集策略：local-first / web+local / web-only
4. 如有视频链接，下载字幕：
   ```bash
   bash tools/research/download_subtitles.sh "{url}" "{skill_dir}/knowledge/subtitles"
   python3 tools/research/srt_to_transcript.py "{subtitle_file}" "{skill_dir}/knowledge/transcripts/{name}.txt"
   ```
5. 按 6 维度研究，至少拆成 3 个文件（每个覆盖 2 维度）：
   - `01_core_profile.md`（维度1 著作 + 维度6 时间线）
   - `02_conversations_and_material.md`（维度2 对话 + 维度4 决策）
   - `03_expression_and_reception.md`（维度3 表达DNA + 维度5 他者视角）
6. 遵守品味原则：长文>金句，争议>共识，变化>固定，一手>二手
7. 信源黑名单：永不引用知乎、微信公众号、百度百科、内容农场
8. 信源优先级：用户本地>一手著作>长访谈>决策记录>社交媒体>外部分析>二手转述
9. 合并 research：`python3 tools/research/merge_research.py "{skill_dir}"`
10. 读取 merged summary，确认 Files≥3, URLs≥2, 无长引用
11. 质量关卡（Phase 1.5）：向用户展示结构化采集摘要，等待确认
12. 冷门人物检测：总来源<10条时，限制心智模型2-3个，标注"基于有限信息"

## budget-unfriendly（深度版）

1. 读取 `prompts/celebrity/budget_unfriendly/research.md` + `references/celebrity_budget_unfriendly_framework.md`
2. 创建目录：额外加 `knowledge/research/reviews`
3. 按 6-track 独立文件结构写 research notes（不可合并）：
   - `01_writings.md` / `02_conversations.md` / `03_expression_dna.md`
   - `04_decisions.md` / `05_external_views.md` / `06_timeline.md`
4. 每条 evidence 标注 source weight (1-7)
5. 合并 research，确认最低门槛：Files≥6, URLs≥8, Primary≥3, Contradictions≥6
6. 质量关卡（Phase 1.5）：展示含 primary 比例、矛盾数、候选 mental models 的摘要
7. 生成 `research_audit.md`，必须明确 PASS/FAIL
8. 提炼关卡（Phase 2.5）：展示候选 mental models（含三重门判定）
9. 生成 `synthesis.md`，做 triple-gate 判断（cross-context recurrence / generative power / exclusivity）
10. 生成 `validation.md`，必须 PASS/FAIL，含 known-answer check + edge-case + voice check + copyright check

## 共同约束

- 外部搜集失败时：明确告知用户，保留已有材料，继续生成但标记 source_grounding 未完成
- 不编造 URL、引用、书名、视频标题
- 不存储完整 transcript/字幕/长段原文
- 只保留结构化摘要、来源元信息和极短引用
