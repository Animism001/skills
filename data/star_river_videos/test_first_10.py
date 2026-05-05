#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import urllib.error
import time
from pathlib import Path
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept": "application/json",
    "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000",
}

def http_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def get_video_cid(bvid):
    try:
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        data = http_get(url)
        
        if data.get("code") == 0:
            video_data = data.get("data", {})
            pages = video_data.get("pages", [])
            if pages:
                cid = pages[0].get("cid")
                title = video_data.get("title", "")
                return {"cid": cid, "title": title, "bvid": bvid}
        return {"error": data.get("message", "获取失败"), "bvid": bvid}
    except Exception as e:
        return {"error": str(e), "bvid": bvid}

def get_subtitles(bvid, cid):
    try:
        url = f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"
        data = http_get(url)
        if data.get("code") == 0:
            player_data = data.get("data", {})
            subtitle_info = player_data.get("subtitle", {})
            if subtitle_info:
                subtitles = subtitle_info.get("subtitles", [])
                return {"bvid": bvid, "cid": cid, "subtitles": subtitles}
        return {"bvid": bvid, "cid": cid, "subtitles": [], "has_subtitles": False}
    except Exception as e:
        return {"bvid": bvid, "error": str(e)}

def download_subtitle(subtitle_url, output_file):
    try:
        req = urllib.request.Request(subtitle_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True, "size": len(content), "file": output_file}
    except Exception as e:
        return {"error": str(e)}

def convert_subtitle_to_srt(subtitle_json_file, output_srt_file):
    try:
        with open(subtitle_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        body = data.get("body", [])
        srt_content = []
        for i, item in enumerate(body, 1):
            from_time = item.get("from", 0)
            to_time = item.get("to", 0)
            content = item.get("content", "")
            from_str = format_timestamp(from_time)
            to_str = format_timestamp(to_time)
            srt_content.append(str(i))
            srt_content.append(f"{from_str} --> {to_str}")
            srt_content.append(content)
            srt_content.append("")
        with open(output_srt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        return {"success": True, "file": output_srt_file}
    except Exception as e:
        return {"error": str(e)}

def format_timestamp(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    output_dir = Path("/workspace/star_river_videos/subtitles")
    output_dir.mkdir(exist_ok=True)
    
    videos_file = Path("/workspace/star_river_videos/all_videos.json")
    
    with open(videos_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        videos = data.get("videos", [])
    
    videos = videos[:10]
    print(f"✅ 找到 {len(videos)} 个视频（测试前10个）")
    
    results = []
    subtitle_count = 0
    
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*70}")
        print(f"处理第 {i}/{len(videos)} 个视频")
        
        bvid = video.get("bvid", "")
        title = video.get("title", "")
        print(f"标题: {title}")
        print(f"BV号: {bvid}")
        
        safe_title = "".join(c if c.isalnum() or c in " _-." else "_" for c in title[:50]).strip()
        
        try:
            print(f"1/3 - 获取CID...")
            cid_result = get_video_cid(bvid)
            
            if "error" in cid_result:
                print(f"❌ 无法获取CID: {cid_result.get('error')}")
                results.append({**video, "has_subtitles": False, "error": cid_result.get('error')})
                time.sleep(random.uniform(1, 2))
                continue
            
            cid = cid_result["cid"]
            print(f"✅ CID: {cid}")
            
            print(f"2/3 - 检查字幕...")
            sub_result = get_subtitles(bvid, cid)
            subtitles = sub_result.get("subtitles", [])
            
            if not subtitles:
                print(f"❌ 没有字幕")
                results.append({**video, "cid": cid, "has_subtitles": False})
                time.sleep(random.uniform(1, 2))
                continue
            
            print(f"✅ 找到 {len(subtitles)} 个字幕")
            
            print(f"3/3 - 下载字幕...")
            subtitle_count += 1
            
            video_subtitles = []
            
            for j, sub in enumerate(subtitles):
                sub_type = sub.get("type", "")
                sub_lan = sub.get("lan_doc", sub.get("lan", ""))
                sub_url = sub.get("subtitle_url", "")
                
                if not sub_url.startswith("http"):
                    sub_url = "https:" + sub_url
                
                print(f"  [{j+1}] 下载 {sub_lan} ({sub_type})...")
                
                json_file = output_dir / f"{safe_title}_{bvid}_{sub_lan}_{j}.json"
                srt_file = output_dir / f"{safe_title}_{bvid}_{sub_lan}_{j}.srt"
                
                download_result = download_subtitle(sub_url, str(json_file))
                
                if download_result.get("success"):
                    print(f"      ✅ 下载成功: {download_result.get('size')} 字节")
                    convert_result = convert_subtitle_to_srt(str(json_file), str(srt_file))
                    if convert_result.get("success"):
                        print(f"      ✅ 转换为SRT: {srt_file.name}")
                    
                    video_subtitles.append({
                        "type": sub_type,
                        "lan": sub_lan,
                        "json_file": str(json_file),
                        "srt_file": str(srt_file),
                        "url": sub_url
                    })
                else:
                    print(f"      ❌ 下载失败: {download_result.get('error')}")
            
            results.append({**video, "cid": cid, "has_subtitles": True, "subtitles": video_subtitles})
            
            print(f"✅ 处理完成! 共 {len(video_subtitles)} 个字幕")
            
        except Exception as e:
            print(f"❌ 处理异常: {e}")
            results.append({**video, "has_subtitles": False, "error": str(e)})
        
        delay = random.uniform(1, 2)
        print(f"😴 等待 {delay:.1f} 秒...")
        time.sleep(delay)
    
    final_result_file = output_dir / "test_10_results.json"
    with open(final_result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total": len(videos),
            "with_subtitles": subtitle_count,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ 测试完成！")
    print(f"总视频数: {len(videos)}")
    print(f"有字幕的视频: {subtitle_count}")
    print(f"结果保存至: {final_result_file}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
