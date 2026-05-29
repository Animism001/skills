# 进化模式指南

## 追加文件

用户提供新文件或文本时：

1. 按 Step 2 的方式读取新内容
2. 根据当前 family 解析 base dir
3. `Read` 现有 `{base_dir}/{slug}/work.md` 和 `persona.md`
4. 使用对应 merger prompt 分析增量内容
5. 存档当前版本：
   ```bash
   python3 tools/version_manager.py --action backup --character {character} --slug {slug} --base-dir {base_dir}
   ```
6. 写 work/persona 增量到临时 patch 文件
7. 调用：
   ```bash
   python3 tools/skill_writer.py \
     --action update \
     --character {character} \
     --slug {slug} \
     --work-patch /tmp/dot_skill_{slug}_work_patch.md \
     --persona-patch /tmp/dot_skill_{slug}_persona_patch.md \
     --base-dir {base_dir}
   ```
8. celebrity 更新后再次执行 quality check

## 对话纠正

用户说"不对"/"应该是"时：

1. 参考 `prompts/correction_handler.md` 识别纠正内容
2. 判断属于 Work（技术/流程）还是 Persona（性格/沟通）

**Work 纠正**：
- 生成 patch 文件（可替换的 `##` section）
- `python3 tools/skill_writer.py --action update --character {character} --slug {slug} --work-patch /tmp/... --base-dir {base_dir}`

**Persona 纠正**：
- 写 correction JSON：`{scene, wrong, correct}` 或 `{"persona_corrections": [{...}]}`
- `python3 tools/skill_writer.py --action update --character {character} --slug {slug} --correction-json /tmp/... --base-dir {base_dir}`

**重要**：不要直接手改 work.md、persona.md、SKILL.md、meta.json，统一通过 writer 更新。

## 管理操作

```bash
# 列出
python3 tools/skill_writer.py --action list --character {colleague|relationship|celebrity} --base-dir {base_dir}

# 回滚
python3 tools/version_manager.py --action rollback --character {character} --slug {slug} --version {version} --base-dir {base_dir}

# 删除
rm -rf {base_dir}/{slug}
```
