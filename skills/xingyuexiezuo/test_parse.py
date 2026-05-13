#!/usr/bin/env python3
import re
import json
from pathlib import Path


def parse_markdown_categories(md_file):
    """解析分类markdown文件,提取视频BV号和分类"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分类列表
    categories = [
        "AI写作技巧", "使用教程", "收益与赚钱", "作者访谈", "创作素材",
        "榜单成绩", "其他", "新手入门", "励志故事", "AI模型评测", "短剧改编"
    ]
    
    videos_by_category = {}
    current_category = None
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        # 检测分类标题
        for cat in categories:
            if line.startswith(f'## {cat}'):
                current_category = cat
                if current_category not in videos_by_category:
                    videos_by_category[current_category] = []
                break
        
        # 提取BV号 (格式: [BVxxxxxx](链接))
        if current_category:
            bv_match = re.search(r'\[BV[0-9A-Za-z]+\]', line)
            if bv_match:
                bv_id = bv_match.group()[1:-1]
                # 提取标题
                parts = line.split('|')
                if len(parts) >= 3:
                    title = parts[2].strip()
                    # 提取发布时间
                    pub_date = None
                    if len(parts) >= 2:
                        pub_date = parts[1].strip()
                    videos_by_category[current_category].append({
                        'bv_id': bv_id,
                        'title': title,
                        'pub_date': pub_date
                    })
    
    return videos_by_category


def main():
    base_dir = Path("/workspace/skills/xingyuexiezuo")
    md_file = base_dir / "星月凌云B站视频目录_分类版.md"
    transcripts_dir = base_dir / "transcripts"
    transcripts_dir.mkdir(exist_ok=True)
    
    # 解析分类
    print("正在解析视频分类...")
    videos_by_category = parse_markdown_categories(md_file)
    
    # 统计并保存
    total_videos = 0
    for cat, videos in videos_by_category.items():
        print(f"{cat}: {len(videos)} 个视频")
        total_videos += len(videos)
        # 创建分类目录
        cat_dir = transcripts_dir / cat
        cat_dir.mkdir(exist_ok=True)
    
    print(f"\n总计: {total_videos} 个视频")
    
    # 保存到JSON文件
    with open(base_dir / "videos_by_category.json", 'w', encoding='utf-8') as f:
        json.dump(videos_by_category, f, ensure_ascii=False, indent=2)
    
    print(f"\n分类信息已保存到: {base_dir / 'videos_by_category.json'}")
    print(f"分类目录已创建在: {transcripts_dir}")


if __name__ == "__main__":
    main()
