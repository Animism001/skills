#!/usr/bin/env python3
"""
优化版小说转剧本脚本：正确识别角色，同时输出JSON和可读剧本
"""

import json
import re
import sys
from pathlib import Path


def extract_text_from_epub(epub_path):
    """简化版，直接读取文本文件"""
    with open(epub_path, 'r', encoding='utf-8') as f:
        return f.read()


def clean_extract_first_improved(original_text):
    """更准确的文本清理和章节识别"""
    # 常见的角色名列表（基于神雕侠侣
    KNOWN_CHARACTERS = [
        "杨过", "小龙女", "郭靖", "黄蓉", "郭芙", "郭襄", "郭破虏",
        "洪七公", "欧阳锋", "黄药师", "一灯大师", "周伯通",
        "金轮法王", "李莫愁", "陆无双", "程英", "耶律齐",
        "武敦儒", "武修文", "赵志敬", "尹志平",
        "达尔巴", "霍都", "藏边五丑",
        "孙不二", "郝大通",
        "丘处机", "王处一", "马钰", "谭处端", "刘处玄",
        "柯镇恶", "朱聪", "韩宝驹", "南希仁", "张阿生", "全金发", "韩小莹"
    ]
    
    # 清理文本
    text = original_text
    
    # 分割章节，从"第.*回"匹配
    section_pattern = re.compile(r'第[一二三四五六七八九十百千万0-9]+回[：:\s]+([^\n]+)')
    
    sections = []
    
    # 找到所有章节匹配
    matches = list(section_pattern.finditer(text))
    )
    sections = []
    
    # 先找到前3个章节
    pos = 0
    for i, match in enumerate(matches):
        if i >= 3:  # 只取前3回
            break
        
        section_start = match.start()
        section_title = match.group(1).strip()
        
        if i + 1 < len(list(section_pattern.finditer(text))):
            next_match = list(section_pattern.finditer(text))[i + 1]
            section_end = next_match.start()
        else:
            section_end = len(text)
        
        section_text = text[section_start:section_end].strip()
        
        sections.append({
            "id": f"第{i+1}回",
            "title": section_title,
            "text": section_text
        })
    
    return sections


def analyze_section_improved(section_text, known_chars):
    """改进的章节分析：正确识别角色名"""
    result = {
        "scenes": [],
        "dialogues": [],
        "characters": {},
        "narrative": [],
        "original": section_text
    }
    
    lines = section_text.split("\n")
    
    current_scene = {"id": f"S1", "type": "narrative", "content": ""}
    
    # 分析对话
    dialogue_matches = []
    
    # 使用正则表达式匹配对话
    # 格式1：角色+：+"内容"
    dialogue_pattern = re.compile(r'([^\s：:""“”]+)\s*[：:]\s*["“]([^"”]+)["”]', re.DOTALL)
    
    # 先识别所有对话
    pos = 0
    while True:
        match = dialogue_pattern.search(section_text, pos)
        if not match:
            break
        
        speaker = match.group(1).strip()
        content = match.group(2).strip()
        
        # 检查是否是角色名（过滤掉“说道”、“笑道”这种
        if speaker.endswith(("道", "说", "笑", "叫", "问", "答", "想", "寻思", "暗道"):
            speaker = speaker[:-1]
        if speaker.endswith(("忽然", "突然", "微微", "轻轻", "大声", "低声", "暗暗", "嘿嘿", "哈哈")):
            speaker = speaker[:-2]
        if len(speaker) > 0:
            # 尝试匹配已知角色
            for known_char in known_chars:
                if known_char in speaker:
                    speaker = known_char
                    break
        
        if len(speaker) > 0:
            dialogue = {
                "speaker": speaker,
                "content": content,
                "position": match.start()
            }
            dialogue_matches.append(dialogue)
            pos = match.end()
        else:
            pos = match.end()
    
    result["dialogues"] = dialogue_matches
    
    # 识别出现在文本中的角色
    for char in known_chars:
        if char in section_text:
            result["characters"][char] = {"name": char, "appearances": []}
    
    # 简单的场景分割
    # 按场景切换来分割文本
    paragraphs = re.split(r'\n\s*\n', section_text)
    scenes = []
    
    for i, para in enumerate(paragraphs):
        if para.strip():
            scene = {
                "id": f"S{i+1}",
                "setting": "",
                "content": para.strip(),
                "dialogues": []
            }
            scenes.append(scene)
    
    result["scenes"] = scenes
    
    return result


def convert_to_json_and_readable(sections, known_chars, title="神雕侠侣", author="金庸"):
    """同时输出JSON和可读剧本"""
    
    # JSON格式
    json_data = {
        "title": title,
        "author": author,
        "format": "剧本",
        "type": "AI·动画(2D)",
        "genre": "武侠",
        "chapters": [],
        "metadata": {
            "total_chapters": len(sections),
            "characters": list(known_chars)
        }
    }
    
    # 可读剧本
    readable = []
    readable.append(f"# {title} - 剧本\n")
    readable.append(f"**作者**: {author}\n")
    readable.append("---\n\n")
    
    for i, section in enumerate(sections):
        analyzed = analyze_section_improved(section["text"], known_chars)
        
        # 处理JSON数据
        chapter_data = {
            "chapter_id": section["id"],
            "chapter_title": section["title"],
            "original_text": section["text"],
            "characters": analyzed["characters"],
            "dialogues": analyzed["dialogues"],
            "scenes": analyzed["scenes"]
        }
        json_data["chapters"].append(chapter_data)
        
        # 处理可读剧本
        readable.append(f"## {section['id']} {section['title']}\n\n")
        
        for scene in analyzed["scenes"]:
            readable.append(f"### 场景 {scene['id']}\n\n")
            
            # 处理场景内容，转换为剧本格式
            # 简单的格式转换
            content = scene["content"]
            
            # 尝试将对话格式化为标准剧本格式
            formatted_content = format_scene_to_script(content, known_chars)
            readable.append(formatted_content)
            readable.append("\n\n")
    
    return json_data, "\n".join(readable)


def format_scene_to_script(text, known_chars):
    """将场景文本格式化为标准剧本"""
    lines = text.split("\n")
    result = []
    
    for line in lines:
        if line.strip():
            # 查找是否有角色对话
            has_dialogue = False
            for char in known_chars:
                if char in line and ("道" in line or "说" in line or "问" in line or "叫" in line):
                    # 找到对话
                    match = re.search(f'({char}.*?)[：:]\s*["“](.*?)["”]', line)
                    if match:
                        speaker = match.group(1)
                        # 清理说话者
                        speaker_clean = char
                        dialogue = match.group(2)
                        
                        result.append(f"{speaker_clean.upper()}")
                        result.append(f"  {dialogue}")
                        has_dialogue = True
                        break
            
            if not has_dialogue:
                # 叙述
                result.append(f"{line.strip()}")
    
    return "\n".join(result)


def main():
    input_path = Path("/workspace/library/神雕侠侣-三联版.txt")
    output_dir = Path("/workspace/projects/shediao-drama")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print("正在读取文本...")
    text = extract_text_from_epub(input_path)
    
    # 角色列表
    known_chars = [
        "杨过", "小龙女", "郭靖", "黄蓉", "郭芙",
        "洪七公", "欧阳锋", "黄药师", "周伯通",
        "金轮法王", "李莫愁", "陆无双", "程英",
        "武敦儒", "武修文", "赵志敬", "尹志平",
        "达尔巴", "藏边五丑"
    ]
    
    print("正在解析章节...")
    sections = clean_extract_first_improved(text)
    
    if len(sections) == 0:
        # 如果自动章节识别失败，手动分块
        print("使用备用章节识别，手动分割...")
        chunks = text.split("\n\n")[:100]
        sections = [
            {
                "id": "第1回",
                "title": "风尘困顿",
                "text": "\n\n".join(chunks)
            }
        ]
    
    print(f"解析了 {len(sections)} 个章节")
    
    print("正在转换...")
    json_data, readable_script = convert_to_json_and_readable(sections, known_chars)
    
    json_output = output_dir / "shediao-script.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    readable_output = output_dir / "shediao-script.md"
    with open(readable_output, 'w', encoding='utf-8') as f:
        f.write(readable_script)
    
    print(f"转换完成！")
    print(f"JSON格式: {json_output}")
    print(f"可读格式: {readable_output}")


if __name__ == '__main__':
    main()
