#!/usr/bin/env python3
"""
literature-to-json-script: 将小说/文学作品逐章节转换为JSON格式剧本，100%保留所有原著内容
"""

import json
import re
import sys
import os
from pathlib import Path


def extract_text_from_epub(epub_path):
    """从EPUB文件中提取纯文本"""
    import zipfile
    import html.parser
    try:
        import ebooklib
        from ebooklib import epub
    except ImportError:
        print("需要安装ebooklib: pip install ebooklib")
        sys.exit(1)
    
    text_chunks = []
    
    class HTMLTextExtractor(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.result = []
        
        def handle_data(self, data):
            if data.strip():
                self.result.append(data.strip())
    
    book = epub.read_epub(epub_path)
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content().decode('utf-8', errors='ignore')
            extractor = HTMLTextExtractor()
            extractor.feed(content)
            text_chunks.append('\n'.join(extractor.result))
    
    return '\n\n'.join(text_chunks)


def read_text_file(file_path):
    """读取文本文件或EPUB"""
    file_path = Path(file_path)
    if file_path.suffix == '.epub':
        return extract_text_from_epub(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def split_into_sections(text, split_by='chapter'):
    """将文本分割成章节/场景"""
    sections = []
    
    if split_by == 'chapter':
        # 常见章节标题模式
        chapter_pattern = re.compile(r'^第[一二三四五六七八九十百千万0-9]+[章节回卷]|^\d+\s*[章节回卷]|^[章节回卷]\s*\d+', re.MULTILINE)
        matches = list(chapter_pattern.finditer(text))
        
        if matches:
            for i, match in enumerate(matches):
                start = match.start()
                if i + 1 < len(matches):
                    end = matches[i + 1].start()
                else:
                    end = len(text)
                sections.append({
                    'section_id': f"第{i+1}章",
                    'section_title': match.group().strip(),
                    'original_text': text[start:end].strip()
                })
        else:
            # 没有找到明显的章节标记，每5000字分割一次
            chunk_size = 5000
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size]
                sections.append({
                    'section_id': f"section_{i//chunk_size + 1}",
                    'section_title': f"Section {i//chunk_size + 1}",
                    'original_text': chunk
                })
    
    elif split_by == 'scene':
        # 简单地按空行分割场景
        paragraphs = re.split(r'\n\s*\n', text)
        for i, para in enumerate(paragraphs):
            if para.strip():
                sections.append({
                    'section_id': f"scene_{i+1}",
                    'section_title': f"Scene {i+1}",
                    'original_text': para
                })
    
    return sections


def analyze_section(section, section_idx):
    """分析单个章节，提取角色、对话、叙述"""
    text = section['original_text']
    chars = list(text)
    
    # 识别对话 - 引号包围的文本
    dialogue_pattern = re.compile(r'["\"](.*?)["\"]', re.DOTALL)
    dialogues = []
    narratives = []
    characters = {}
    
    # 先找出所有引号位置
    quote_positions = []
    i = 0
    while i < len(chars):
        if chars[i] in ['"', '\"', '“', '”']:
            start = i
            i += 1
            while i < len(chars) and chars[i] not in ['"', '\"', '“', '”']:
                i += 1
            if i < len(chars):
                quote_positions.append((start, i + 1))
                i += 1
        i += 1
    
    # 分割对话和叙述
    last_pos = 0
    for start, end in quote_positions:
        if last_pos < start:
            # 对话前的叙述
            narrative_text = text[last_pos:start]
            if narrative_text.strip():
                narratives.append({
                    'type': 'description',
                    'content': narrative_text,
                    'position': last_pos
                })
        
        # 对话
        dialogue_text = text[start+1:end-1]
        speaker = ""
        # 尝试识别说话人
        prev_context = text[max(0, last_pos - 50):start]
        speaker_match = re.search(r'(\w+)[：:]', prev_context)
        if speaker_match:
            speaker = speaker_match.group(1)
        
        dialogues.append({
            'speaker': speaker,
            'content': dialogue_text,
            'position': start
        })
        
        # 记录角色
        if speaker:
            if speaker not in characters:
                characters[speaker] = {
                    'name': speaker,
                    'speeches': [],
                    'actions': [],
                    'appearances': []
                }
            characters[speaker]['speeches'].append({
                'line': dialogue_text,
                'position': start
            })
            characters[speaker]['appearances'].append(start)
        
        last_pos = end
    
    # 最后的叙述
    if last_pos < len(text):
        narratives.append({
            'type': 'description',
            'content': text[last_pos:],
            'position': last_pos
        })
    
    # 转换为列表
    char_list = list(characters.values())
    
    return {
        **section,
        'characters': char_list,
        'dialogues': dialogues,
        'narrative': narratives
    }


def convert_to_json(text, title="", author="", version="", split_by='chapter'):
    """转换文本为JSON剧本"""
    sections = split_into_sections(text, split_by)
    
    json_output = {
        "title": title,
        "author": author,
        "version": version,
        "total_sections": len(sections),
        "sections": [],
        "metadata": {
            "total_characters": 0,
            "total_words": len(text.split()),
            "extraction_date": "2026-05-31"
        }
    }
    
    all_characters = set()
    
    for i, section in enumerate(sections):
        analyzed = analyze_section(section, i)
        json_output['sections'].append(analyzed)
        
        for char in analyzed['characters']:
            all_characters.add(char['name'])
    
    json_output['metadata']['total_characters'] = len(all_characters)
    
    return json_output


def main():
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <文件路径> [章节分割方式] [标题] [作者]")
        print(f"章节分割方式: chapter (默认) | scene")
        sys.exit(1)
    
    file_path = sys.argv[1]
    split_by = sys.argv[2] if len(sys.argv) > 2 else 'chapter'
    title = sys.argv[3] if len(sys.argv) > 3 else Path(file_path).stem
    author = sys.argv[4] if len(sys.argv) > 4 else ""
    
    print(f"正在读取文件: {file_path}")
    text = read_text_file(file_path)
    
    print(f"正在转换为JSON，分割方式: {split_by}")
    json_result = convert_to_json(text, title=title, author=author, split_by=split_by)
    
    output_file = Path(file_path).stem + ".json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_result, f, ensure_ascii=False, indent=2)
    
    print(f"转换完成，输出: {output_file}")
    print(f"总章节数: {json_result['total_sections']}")
    print(f"总角色数: {json_result['metadata']['total_characters']}")
    print(f"总字数: {json_result['metadata']['total_words']}")


if __name__ == '__main__':
    main()
