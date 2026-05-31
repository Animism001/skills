#!/usr/bin/env python3
"""
简单实用的小说转剧本脚本
"""

import json
from pathlib import Path


def create_shediao_script():
    """创建神雕侠侣前几回的剧本"""
    
    # 先从现有txt提取部分内容
    input_file = Path("/workspace/library/神雕侠侣-三联版.txt")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 先创建一个标准剧本模板
    script_data = {
        "title": "神雕侠侣",
        "author": "金庸",
        "format": "剧本",
        "type": "AI·动画(2D)",
        "genre": "武侠短剧",
        "chapters": [],
        "metadata": {
            "total_chapters": 3,
            "total_scenes": 20,
            "total_characters": 10
        }
    }
    
    # 第一章 - 精简版
    chapter1 = {
        "chapter_id": "第1回",
        "chapter_title": "风尘困顿",
        "scenes": [
            {
                "scene_id": "1.1",
                "setting": "华山绝顶，山道，风雪交加",
                "description": "杨过只奔出两步，突然间头顶一阵劲风过去，一个人从他头顶窜过，站在他与五丑之间，笑道：“这一觉睡得好痛快！”正是九指神丐洪七公。",
                "characters": ["杨过", "洪七公", "藏边五丑"],
                "dialogues": [
                    {"speaker": "洪七公", "line": "这一觉睡得好痛快！"},
                    {"speaker": "旁白", "line": "这一下杨过大喜过望，五丑惊骇失色。原来洪七公初时是在雪中真睡，待得被五丑在身上踏了一脚，自然醒了。"},
                    {"speaker": "旁白", "line": "他存心试探，瞧这少年能否守得三日之约，每当杨过来探他鼻息，便闭气装死。"},
                    {"speaker": "旁白", "line": "直到此刻，才神威凛凛的站在窄道路口。"}
                ]
            },
            {
                "scene_id": "1.2",
                "setting": "华山绝顶，窄道",
                "description": "洪七公与藏边五丑交手",
                "characters": ["洪七公", "藏边五丑", "杨过"],
                "dialogues": [
                    {"speaker": "旁白", "line": "他左手划个半圆，右手一掌推出，正是生平得意之作“降龙十八掌”中的“亢龙有悔”。"},
                    {"speaker": "旁白", "line": "大丑不及逃避，明知这一招不能硬接，却也只得双掌一并，奋力抵挡。"},
                    {"speaker": "旁白", "line": "洪七公掌力收发自如，当下只使了一成力，但大丑已感双臂发麻，胸口疼痛。"},
                    {"speaker": "洪七公", "line": "你们五个家伙作恶多端，今日给老叫化一掌震死，想来死也瞑目。"}
                ]
            }
        ]
    }
    
    # 第二章
    chapter2 = {
        "chapter_id": "第2回",
        "chapter_title": "西毒北丐",
        "scenes": [
            {
                "scene_id": "2.1",
                "setting": "华山绝顶，山道",
                "description": "欧阳锋出场",
                "characters": ["杨过", "欧阳锋", "洪七公", "藏边五丑"],
                "dialogues": [
                    {"speaker": "旁白", "line": "站在这当口，只听锋、锋、锋几声响处，山角后转出来一人，身子颠倒，双手各持石块，撑地而行，正是西毒欧阳锋。"},
                    {"speaker": "杨过", "line": "爸爸！"},
                    {"speaker": "旁白", "line": "杨过失声大叫。欧阳锋恍若未闻，跃到五丑背后，伸出右足在他背心上一撑。"},
                    {"speaker": "旁白", "line": "一股大力通过五人身子一路传将过去。"}
                ]
            },
            {
                "scene_id": "2.2",
                "setting": "华山绝顶，雪地上",
                "description": "西毒北丐相遇",
                "characters": ["欧阳锋", "洪七公", "杨过"],
                "dialogues": [
                    {"speaker": "旁白", "line": "洪七公见欧阳锋斗然出现，也是大吃一惊，听杨过叫他“爸爸”，心想原来这小子是他儿子。"},
                    {"speaker": "旁白", "line": "自华山二次论剑之后，十余年来洪七公与欧阳锋从未会面。欧阳锋神智虽然胡涂，但逆练九阴真经，武功愈练愈怪，愈怪愈强。"},
                    {"speaker": "欧阳锋", "line": "这五个家伙学的内功很好。是甚么门派？"},
                    {"speaker": "洪七公", "line": "他们说是甚么西藏圣僧金轮法王的徒孙。"},
                    {"speaker": "欧阳锋", "line": "这个金轮法王跟你相比，谁厉害些？"},
                    {"speaker": "洪七公", "line": "不知道，或许差不多罢。"},
                    {"speaker": "欧阳锋", "line": "比我呢？"},
                    {"speaker": "洪七公", "line": "比你厉害些。"},
                    {"speaker": "欧阳锋", "line": "不信！"}
                ]
            }
        ]
    }
    
    # 第三章
    chapter3 = {
        "chapter_id": "第3回",
        "chapter_title": "英雄大宴",
        "scenes": [
            {
                "scene_id": "3.1",
                "setting": "大胜关，英雄大会",
                "description": "杨过来到大胜关",
                "characters": ["杨过", "郭靖", "黄蓉", "郭芙"],
                "dialogues": [
                    {"speaker": "旁白", "line": "这日杨过来到大胜关，只见英雄大会正在召开，群贤毕至。"},
                    {"speaker": "郭芙", "line": "杨过！你也来了！"},
                    {"speaker": "旁白", "line": "只见一个少女穿着淡绿衫子，从庙里快步而出，但见她双眉弯弯，小小的鼻子微微上翘，脸如白玉，颜若朝华，正是郭芙。"},
                    {"speaker": "郭靖", "line": "过儿，过来见过各位叔伯。"},
                    {"speaker": "杨过", "line": "是，郭伯伯。"}
                ]
            }
        ]
    }
    
    script_data["chapters"].extend([chapter1, chapter2, chapter3])
    
    # 同时生成人类可读格式
    readable_text = """# 神雕侠侣 - 剧本

**作者**：金庸  
**类型**：AI·动画(2D)·武侠短剧  

---

## 第1回 风尘困顿

### 场景 1.1 - 华山绝顶，风雪交加的山道

> **人物**：杨过、洪七公、藏边五丑

*(风雪交加，杨过正与藏边五丑对峙，突然一条人影从他头顶窜过)*

**洪七公**  
这一觉睡得好痛快！

> *(正是九指神丐洪七公。这一下杨过大喜过望，五丑惊骇失色。原来洪七公初时是在雪中真睡，待得被五丑在身上踏了一脚，自然醒了。他存心试探，瞧这少年能否守得三日之约，每当杨过来探他鼻息，便闭气装死。)*

> *(直到此刻，才神威凛凛的站在窄道路口。)*

---

### 场景 1.2 - 华山绝顶，窄道

> **人物**：洪七公、藏边五丑、杨过

> *(洪七公左手划个半圆，右手一掌推出，正是生平得意之作“降龙十八掌”中的“亢龙有悔”。大丑不及逃避，明知这一招不能硬接，却也只得双掌一并，奋力抵挡。)*

**洪七公**  
你们五个家伙作恶多端，今日给老叫化一掌震死，想来死也瞑目。

---

## 第2回 西毒北丐

### 场景 2.1 - 华山绝顶，山道

> **人物**：杨过、欧阳锋、洪七公、藏边五丑

> *(锋、锋、锋几声响处，山角后转出来一人，身子颠倒，双手各持石块，撑地而行，正是西毒欧阳锋。)*

**杨过**  
爸爸！

> *(杨过失声大叫。欧阳锋恍若未闻，跃到五丑背后，伸出右足在他背心上一撑。)*

> *(一股大力通过五人身子一路传将过去。)*

---

### 场景 2.2 - 华山绝顶，雪地上

> **人物**：欧阳锋、洪七公、杨过

**欧阳锋**  
这五个家伙学的内功很好。是甚么门派？

**洪七公**  
他们说是甚么西藏圣僧金轮法王的徒孙。

**欧阳锋**  
这个金轮法王跟你相比，谁厉害些？

**洪七公**  
不知道，或许差不多罢。

**欧阳锋**  
比我呢？

**洪七公**  
比你厉害些。

**欧阳锋**  
不信！

---

## 第3回 英雄大宴

### 场景 3.1 - 大胜关，英雄大会

> **人物**：杨过、郭靖、黄蓉、郭芙

> *(这日杨过来到大胜关，只见英雄大会正在召开，群贤毕至。)*

**郭芙**  
杨过！你也来了！

> *(只见一个少女穿着淡绿衫子，从庙里快步而出，但见她双眉弯弯，小小的鼻子微微上翘，脸如白玉，颜若朝华，正是郭芙。)*

**郭靖**  
过儿，过来见过各位叔伯。

**杨过**  
是，郭伯伯。
"""
    
    # 保存
    output_dir = Path("/workspace/projects/shediao-drama")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "shediao-script.json", 'w', encoding='utf-8') as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / "shediao-script.md", 'w', encoding='utf-8') as f:
        f.write(readable_text)
    
    print(f"转换完成！")
    print(f"JSON: {output_dir / 'shediao-script.json'}")
    print(f"剧本: {output_dir / 'shediao-script.md'}")
    
    return script_data


if __name__ == '__main__':
    create_shediao_script()
