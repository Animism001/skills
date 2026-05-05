#!/usr/bin/env python3
import json
import subprocess
import time
import random
import re
from pathlib import Path

# 常用的User-Agent列表
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def run_yt_dlp(url, extra_args=None):
    ua = get_random_user_agent()
    args = [
        "yt-dlp",
        "--user-agent", ua,
        "--referer", "https://www.bilibili.com/",
        "--add-header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "--add-header", "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "--add-header", "Accept-Encoding: gzip, deflate, br",
        "--add-header", "Connection: keep-alive",
        "--add-header", "Sec-Fetch-Dest: document",
        "--add-header", "Sec-Fetch-Mode: navigate",
        "--add-header", "Sec-Fetch-Site: same-origin",
        "--add-header", "Sec-Fetch-User: ?1",
        "--add-header", "Upgrade-Insecure-Requests: 1"
    ]
    
    if extra_args:
        args.extend(extra_args)
    
    args.append(url)
    
    print(f"  [yt-dlp] 请求 {url[:50]}...")
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"

def main():
    output_dir = Path("/workspace/star_river_videos/subtitles")
    output_dir.mkdir(exist_ok=True)
    
    videos_file = Path("/workspace/star_river_videos/all_videos.json")
    
    if not videos_file.exists():
        print(f"❌ 找不到视频文件: {videos_file}")
        return
    
    with open(videos_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        videos = data.get("videos", [])
    
    print(f"✅ 找到 {len(videos)} 个视频")
    
    # 先尝试获取前5个视频，测试一下
    test_videos = videos[:5]
    print(f"🧪 先测试前 {len(test_videos)} 个视频...")
    
    results = []
    
    for i, video in enumerate(test_videos, 1):
        print(f"\n{'='*70}")
        print(f"处理第 {i}/{len(test_videos)} 个视频")
        print(f"标题: {video.get('title')}")
        print(f"链接: {video.get('url')}")
        print(f"{'='*70}")
        
        bvid = video.get("bvid", "")
        title = video.get("title", "unknown")
        url = video.get("url", "")
        
        if not bvid or not url:
            print("⚠️ 缺少必要信息，跳过")
            continue
        
        # 安全的文件名
        safe_title = "".join(c if c.isalnum() or c in " _-." else "_" for c in title[:50]).strip()
        subtitle_file = output_dir / f"{safe_title}_{bvid}.srt"
        info_file = output_dir / f"{safe_title}_{bvid}_info.json"
        temp_pattern = str(output_dir / f"{safe_title}_{bvid}")
        
        if subtitle_file.exists() and subtitle_file.stat().st_size > 0:
            print(f"✅ 字幕已存在，跳过")
            continue
        
        try:
            print("🔍 检查并下载字幕...")
            
            success, stdout, stderr = run_yt_dlp(url, [
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs", "zh-CN,zh-TW,zh-Hans,zh,ai-zh,en",
                "--convert-subs", "srt",
                "-o", f"{temp_pattern}.%(ext)s"
            ])
            
            # 查找下载的文件
            downloaded_files = list(output_dir.glob(f"{safe_title}_{bvid}*.srt"))
            
            if downloaded_files:
                downloaded_file = downloaded_files[0]
                if downloaded_file != subtitle_file:
                    downloaded_file.rename(subtitle_file)
                
                print(f"✅ 字幕下载成功: {subtitle_file.name}")
                
                with open(subtitle_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                info = {
                    "title": title,
                    "bvid": bvid,
                    "url": url,
                    "author": video.get("author"),
                    "play": video.get("play"),
                    "duration": video.get("duration"),
                    "pubdate": video.get("pubdate"),
                    "subtitle_file": str(subtitle_file),
                    "has_subtitle": len(content.strip()) > 0,
                    "subtitle_length": len(content)
                }
                
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                
                results.append(info)
                print(f"📄 字幕大小: {len(content)} 字符")
                
                # 预览前几行
                preview_lines = content.split('\n')[:10]
                print(f"📋 字幕预览:")
                for line in preview_lines:
                    if line.strip():
                        print(f"   {line[:80]}")
            else:
                print("❌ 没有找到字幕")
                
                info = {
                    "title": title,
                    "bvid": bvid,
                    "url": url,
                    "has_subtitle": False,
                    "error": "No subtitles available",
                    "stdout": stdout[:500],
                    "stderr": stderr[:500]
                }
                results.append(info)
                
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                
                # 打印一些调试信息
                if stdout:
                    print(f"  stdout: {stdout[:200]}")
                if stderr:
                    print(f"  stderr: {stderr[:200]}")
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            info = {
                "title": title,
                "bvid": bvid,
                "url": url,
                "has_subtitle": False,
                "error": str(e)
            }
            results.append(info)
            
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
        
        # 随机延迟，避免请求过快
        delay = random.uniform(3, 8)
        print(f"😴 等待 {delay:.1f} 秒...")
        time.sleep(delay)
    
    # 统计
    print(f"\n{'='*70}")
    print("✅ 测试完成！")
    success_count = sum(1 for r in results if r.get("has_subtitle", False))
    print(f"成功获取字幕: {success_count}/{len(test_videos)}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*70}")
    
    final_result_file = output_dir / "test_results.json"
    with open(final_result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(test_videos),
            "success": success_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
