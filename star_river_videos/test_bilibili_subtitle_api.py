#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import urllib.error
import time

# 使用与bilibili-search相同的headers
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
    """获取视频的cid（需要cid才能获取字幕）"""
    try:
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        data = http_get(url)
        
        if data.get("code") == 0:
            video_data = data.get("data", {})
            
            # 查找第一个cid
            pages = video_data.get("pages", [])
            if pages:
                cid = pages[0].get("cid")
                title = video_data.get("title", "")
                return {"cid": cid, "title": title, "bvid": bvid}
        
        return {"error": data.get("message", "获取失败")}
    
    except Exception as e:
        return {"error": str(e)}

def get_subtitles(bvid, cid):
    """获取字幕列表"""
    try:
        url = f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"
        data = http_get(url)
        
        if data.get("code") == 0:
            player_data = data.get("data", {})
            subtitle_info = player_data.get("subtitle", {})
            
            if subtitle_info:
                subtitles = subtitle_info.get("subtitles", [])
                return {"bvid": bvid, "cid": cid, "subtitles": subtitles}
        
        return {"error": data.get("message", "获取失败"), "has_subtitles": False}
    
    except Exception as e:
        return {"error": str(e)}

def download_subtitle(subtitle_url, output_file):
    """下载字幕"""
    try:
        req = urllib.request.Request(subtitle_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {"success": True, "size": len(content), "file": output_file}
    
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🔍 测试B站字幕API...")
    
    # 先测试一个视频
    test_bvid = "BV1FhoUB1E78"
    print(f"\n1. 测试获取视频cid - {test_bvid}")
    cid_result = get_video_cid(test_bvid)
    print(json.dumps(cid_result, ensure_ascii=False, indent=2))
    
    if cid_result.get("cid"):
        cid = cid_result["cid"]
        print(f"\n2. 获取字幕列表 - cid: {cid}")
        sub_result = get_subtitles(test_bvid, cid)
        print(json.dumps(sub_result, ensure_ascii=False, indent=2))
        
        if sub_result.get("subtitles"):
            print(f"\n✅ 找到 {len(sub_result['subtitles'])} 个字幕!")
            
            for i, sub in enumerate(sub_result['subtitles']):
                print(f"\n  [{i}] {sub.get('lan_doc', sub.get('lan', ''))}")
                print(f"      类型: {sub.get('type', '')}")
                print(f"      URL: {sub.get('subtitle_url', '')}")

if __name__ == "__main__":
    main()
