#!/usr/bin/env python3
import json
import subprocess
import os
import time
from pathlib import Path

def main():
    # 创建输出目录
    output_dir = Path("/workspace/star_river_videos/subtitles")
    output_dir.mkdir(exist_ok=True)
    
    # 读取视频列表
    videos_file = Path("/workspace/star_river_videos/all_videos.json")
    
    if not videos_file.exists():
        print(f"❌ 找不到视频文件: {videos_file}")
        return
    
    with open(videos_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        videos = data.get("videos", [])
    
    print(f"✅ 找到 {len(videos)} 个视频")
    
    # 统计
    results = []
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*60}")
        print(f"处理第 {i}/{len(videos)} 个视频")
        print(f"标题: {video.get('title')}")
        print(f"链接: {video.get('url')}")
        print(f"{'='*60}")
        
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
        
        # 跳过已处理
        if subtitle_file.exists() and subtitle_file.stat().st_size > 0:
            print(f"✅ 字幕已存在，跳过")
            continue
        
        try:
            # 先检查可用字幕
            print("🔍 检查字幕...")
            check_cmd = ["yt-dlp", "--list-subs", url]
            result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=60)
            
            # 尝试下载字幕（优先CC字幕）
            print("📥 下载字幕...")
            
            # 先尝试CC字幕
            download_cmd = [
                "yt-dlp",
                "--skip-download",
                "--write-subs",
                "--sub-langs", "zh-CN,zh-TW,zh-Hans,zh,ai-zh",
                "--convert-subs", "srt",
                "-o", str(subtitle_file.with_suffix(".%(ext)s")),
                url
            ]
            
            subprocess.run(download_cmd, capture_output=True, text=True, timeout=120)
            
            # 查找下载的文件
            downloaded_files = list(output_dir.glob(f"*{bvid}*.srt"))
            
            if downloaded_files:
                # 如果有多个，选择第一个
                downloaded_file = downloaded_files[0]
                if downloaded_file != subtitle_file:
                    downloaded_file.rename(subtitle_file)
                
                print(f"✅ 字幕下载成功: {subtitle_file.name}")
                
                # 读取字幕内容
                with open(subtitle_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 保存信息
                info = {
                    "title": title,
                    "bvid": bvid,
                    "url": url,
                    "author": video.get("author"),
                    "play": video.get("play"),
                    "duration": video.get("duration"),
                    "pubdate": video.get("pubdate"),
                    "subtitle_file": str(subtitle_file),
                    "has_subtitle": len(content.strip()) > 0
                }
                
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                
                results.append(info)
                
                # 简要统计
                print(f"📄 字幕大小: {len(content)} 字符")
                
                # 保存进度
                progress_file = output_dir / "progress.json"
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "total": len(videos),
                        "processed": i,
                        "success": len(results)
                    }, f, ensure_ascii=False, indent=2)
            else:
                print("❌ 没有找到字幕")
                
                # 保存失败记录
                info = {
                    "title": title,
                    "bvid": bvid,
                    "url": url,
                    "has_subtitle": False,
                    "error": "No subtitles available"
                }
                results.append(info)
                
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            # 保存错误记录
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
        
        # 避免请求过快
        time.sleep(2)
    
    # 最终统计
    print(f"\n{'='*60}")
    print("✅ 处理完成！")
    success_count = sum(1 for r in results if r.get("has_subtitle", False))
    print(f"成功获取字幕: {success_count}/{len(videos)}")
    print(f"输出目录: {output_dir}")
    print(f"{'='*60}")
    
    # 保存最终结果
    final_result_file = output_dir / "all_results.json"
    with open(final_result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(videos),
            "success": success_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
