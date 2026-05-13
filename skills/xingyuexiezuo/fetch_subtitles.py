#!/usr/bin/env python3
import os
import re
import json
import subprocess
import requests
from pathlib import Path


def get_subtitles_from_bilibili(bv_id):
    """从B站API获取字幕"""
    # 首先获取视频信息
    video_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # 获取视频信息
        resp = requests.get(video_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None, f"无法获取视频信息: {resp.status_code}"
        
        data = resp.json()
        if data.get('code') != 0:
            return None, f"API返回错误: {data.get('message')}"
        
        video_data = data.get('data', {})
        aid = video_data.get('aid')
        cid = video_data.get('cid')
        
        if not aid or not cid:
            return None, "无法获取aid或cid"
        
        # 获取字幕列表
        subtitle_url = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
        resp = requests.get(subtitle_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None, f"无法获取字幕列表: {resp.status_code}"
        
        data = resp.json()
        if data.get('code') != 0:
            return None, f"字幕API返回错误: {data.get('message')}"
        
        subtitle_info = data.get('data', {}).get('subtitle', {})
        subtitles = subtitle_info.get('subtitles', [])
        
        if not subtitles:
            return None, "该视频没有字幕"
        
        # 下载第一个字幕
        sub = subtitles[0]
        sub_url = f"https:{sub.get('subtitle_url')}"
        resp = requests.get(sub_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None, f"无法下载字幕: {resp.status_code}"
        
        # 解析字幕JSON
        subtitle_json = resp.json()
        body = subtitle_json.get('body', [])
        
        # 转换成纯文本
        text_lines = []
        for item in body:
            text_lines.append(item.get('content', ''))
        
        full_text = '\n'.join(text_lines)
        return full_text, None
        
    except Exception as e:
        return None, str(e)


def process_videos():
    base_dir = Path("/workspace/skills/xingyuexiezuo")
    json_file = base_dir / "videos_by_category.json"
    transcripts_dir = base_dir / "transcripts"
    
    # 加载分类信息
    with open(json_file, 'r', encoding='utf-8') as f:
        videos_by_category = json.load(f)
    
    # 统计
    total = 0
    success = 0
    failed = 0
    
    # 逐个处理
    for category, videos in videos_by_category.items():
        cat_dir = transcripts_dir / category
        print(f"\n=== 处理分类: {category} ===")
        
        for video in videos:
            bv_id = video['bv_id']
            title = video['title']
            output_file = cat_dir / f"{bv_id}.txt"
            
            if output_file.exists():
                print(f"已存在,跳过: {bv_id}")
                success += 1
                total += 1
                continue
            
            print(f"\n处理: {bv_id} - {title[:50]}...")
            total += 1
            
            # 尝试获取B站字幕
            text, error = get_subtitles_from_bilibili(bv_id)
            
            if text:
                # 保存字幕
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"标题: {title}\n")
                    f.write(f"BV号: {bv_id}\n")
                    f.write(f"分类: {category}\n")
                    f.write("="*50 + "\n\n")
                    f.write(text)
                print(f"✓ 成功获取字幕: {output_file}")
                success += 1
            else:
                print(f"✗ 失败: {error}")
                failed += 1
    
    print(f"\n=== 完成 ===")
    print(f"总计: {total}")
    print(f"成功: {success}")
    print(f"失败: {failed}")


if __name__ == "__main__":
    process_videos()
