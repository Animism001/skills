#!/usr/bin/env python3
import requests
import json
from pathlib import Path


def get_video_subtitle(bvid):
    """从B站API获取字幕"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com'
    }
    
    try:
        # 获取视频信息
        view_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        resp = requests.get(view_url, headers=headers, timeout=15)
        data = resp.json()
        
        if data.get('code') != 0:
            return None, f"获取视频信息失败: {data.get('message')}"
        
        video_data = data.get('data', {})
        aid = video_data.get('aid')
        cid = video_data.get('cid')
        title = video_data.get('title')
        
        print(f"  视频标题: {title}")
        print(f"  aid={aid}, cid={cid}")
        
        # 获取字幕
        subtitle_url = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
        resp = requests.get(subtitle_url, headers=headers, timeout=15)
        data = resp.json()
        
        if data.get('code') != 0:
            return None, f"获取字幕失败: {data.get('message')}"
        
        subtitle_info = data.get('data', {}).get('subtitle', {})
        subtitles = subtitle_info.get('subtitles', [])
        
        if not subtitles:
            # 尝试AI字幕
            print(f"  无官方字幕,检查AI字幕...")
            ai_subtitle = subtitle_info.get('ai_subtitle')
            if ai_subtitle:
                print(f"  发现AI字幕!")
                return ai_subtitle, None
            return None, "该视频没有字幕"
        
        # 下载第一个字幕
        sub = subtitles[0]
        sub_url = f"https:{sub.get('subtitle_url')}"
        print(f"  发现字幕: {sub.get('lan_doc')}")
        
        resp = requests.get(sub_url, headers=headers, timeout=15)
        subtitle_json = resp.json()
        
        # 解析字幕
        body = subtitle_json.get('body', [])
        text_lines = [item.get('content', '') for item in body]
        
        return '\n'.join(text_lines), None
        
    except Exception as e:
        return None, str(e)


# 测试几个视频
test_bvids = [
    'BV1JoAozHEdk',  # Claude4.6写小说能力如何
    'BV17xynBwE4b',  # 都市高武新书榜第一
    'BV1pFoeB6ELF',  # 真实采访AI写作都市高武
]

print("检查视频字幕...\n")

for bvid in test_bvids:
    print(f"检查 {bvid}:")
    text, error = get_video_subtitle(bvid)
    if text:
        print(f"  ✓ 成功! 字幕长度: {len(text)} 字符")
        # 保存测试
        with open(f"/tmp/{bvid}_subtitle.txt", 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  已保存到 /tmp/{bvid}_subtitle.txt")
    else:
        print(f"  ✗ 失败: {error}")
    print()
