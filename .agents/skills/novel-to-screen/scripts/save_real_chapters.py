#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保存神雕侠侣真实章节内容
"""
import re
from pathlib import Path


def save_chapters():
    input_path = Path("/workspace/library/神雕侠侣-三联版.txt")
    output_dir = Path("/workspace/projects/shediao-drama")
    output_dir.mkdir(exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配章节标题
    chapter_pattern = re.compile(r'^(第\s+\S+\s+回\s+.+)$', re.MULTILINE)
    matches = list(chapter_pattern.finditer(content))
    
    print(f"找到 {len(matches)//2} 个章节")
    
    # 分割章节
    chapters = []
    for i in range(0, len(matches), 2):  # 每2个相同标题
        start_match = matches[i]
        if i+1 < len(matches):
            end_match = matches[i+1]
            start = start_match.start()
            if i+2 < len(matches):
                end = matches[i+2].start()
            else:
                end = len(content)
            chapter_title = start_match.group(1).strip()
            chapter_content = content[start:end].strip()
            chapters.append((chapter_title, chapter_content))
    
    # 保存完整原文
    with open(output_dir / "完整原文.txt", 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 保存各个章节
    for i, (title, text) in enumerate(chapters, 1):
        chapter_file = output_dir / f"第{i}回_{title.replace(' ', '').replace('　', '')}.txt"
        with open(chapter_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"已保存: {chapter_file}")
    
    print("\n完成！共保存了", len(chapters), "个章节")


if __name__ == '__main__':
    save_chapters()
