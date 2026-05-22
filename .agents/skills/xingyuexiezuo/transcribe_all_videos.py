#!/usr/bin/env python3
import os
import re
import json
import subprocess
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
                    videos_by_category[current_category].append({
                        'bv_id': bv_id,
                        'title': title
                    })
    
    return videos_by_category


def download_and_transcribe(bv_id, output_dir):
    """下载并转录单个视频"""
    bvid = bv_id
    url = f"https://www.bilibili.com/video/{bvid}"
    
    # 创建临时目录
    temp_dir = Path(output_dir) / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    audio_file = temp_dir / f"{bvid}.m4a"
    transcript_file = Path(output_dir) / f"{bvid}.txt"
    
    if transcript_file.exists():
        print(f"转录文件已存在: {transcript_file}, 跳过")
        return True
    
    try:
        # 使用yt-dlp只下载音频
        print(f"正在下载音频: {bvid}")
        subprocess.run([
            'yt-dlp',
            '-x',  # 只提取音频
            '--audio-format', 'm4a',
            '-o', str(audio_file),
            url
        ], check=True, capture_output=True, text=True)
        
        # 使用whisper转录
        print(f"正在转录: {bvid}")
        result = subprocess.run([
            'whisper',
            str(audio_file),
            '--language', 'Chinese',
            '--model', 'base',
            '--output_format', 'txt',
            '--output_dir', str(temp_dir)
        ], check=True, capture_output=True, text=True)
        
        # 移动转录文件
        generated_txt = temp_dir / f"{bvid}.m4a.txt"
        if generated_txt.exists():
            import shutil
            shutil.move(str(generated_txt), str(transcript_file))
            print(f"转录完成: {transcript_file}")
        
        # 清理音频文件
        if audio_file.exists():
            audio_file.unlink()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"处理 {bvid} 时出错: {e.stderr}")
        return False


def main():
    # 设置目录
    base_dir = Path("/workspace/skills/xingyuexiezuo")
    md_file = base_dir / "星月凌云B站视频目录_分类版.md"
    transcripts_dir = base_dir / "transcripts"
    transcripts_dir.mkdir(exist_ok=True)
    
    # 解析分类
    print("正在解析视频分类...")
    videos_by_category = parse_markdown_categories(md_file)
    
    # 统计
    total_videos = 0
    for cat, videos in videos_by_category.items():
        print(f"{cat}: {len(videos)} 个视频")
        total_videos += len(videos)
    print(f"\n总计: {total_videos} 个视频\n")
    
    # 逐个处理
    for category, videos in videos_by_category.items():
        # 创建分类目录
        cat_dir = transcripts_dir / category
        cat_dir.mkdir(exist_ok=True)
        
        print(f"\n=== 处理分类: {category} ===")
        for video in videos:
            print(f"\n处理视频: {video['title']} ({video['bv_id']})")
            success = download_and_transcribe(video['bv_id'], str(cat_dir))
            if not success:
                print(f"失败: {video['bv_id']}")
    
    print("\n所有处理完成!")


if __name__ == "__main__":
    main()
