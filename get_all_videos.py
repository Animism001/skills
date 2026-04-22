#!/usr/bin/env python3
import sys
import json
import time
import urllib.request
import urllib.parse

def search_videos_by_author(mid: int, max_pages: int = 10) -> list:
    """通过搜索获取指定作者的所有视频"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Accept": "application/json",
        "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000",
    }
    
    all_videos = []
    seen_bvids = set()
    
    # 首先通过搜索"星月凌云"来获取视频
    keywords = ["星月凌云", "-星月凌云-", "星月写作"]
    
    for keyword in keywords:
        for page in range(1, max_pages + 1):
            time.sleep(0.5)
            
            params = urllib.parse.urlencode({
                "keyword": keyword,
                "page": page,
                "pagesize": 50,
                "search_type": "video",
                "order": "pubdate",
            })
            url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
            
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                print(f"搜索失败: {e}")
                continue
            
            if data.get("code") != 0:
                print(f"搜索错误: {data.get('message')}")
                continue
            
            results = data.get("data", {}).get("result", [])
            if not results:
                break
            
            for item in results:
                item_mid = item.get("mid")
                if item_mid == mid:
                    bvid = item.get("bvid", "")
                    if bvid in seen_bvids:
                        continue
                    
                    seen_bvids.add(bvid)
                    all_videos.append({
                        "bvid": bvid,
                        "url": f"https://www.bilibili.com/video/{bvid}",
                        "title": item.get("title", "").replace('<em class="keyword">', "").replace('</em>', ""),
                        "author": item.get("author"),
                        "play": item.get("play"),
                        "danmaku": item.get("video_review"),
                        "favorites": item.get("favorites"),
                        "like": item.get("like"),
                        "pubdate": item.get("pubdate"),
                        "duration": item.get("duration"),
                    })
            
            print(f"关键词 '{keyword}' 第 {page} 页获取了 {len(results)} 个视频，已收集 {len(all_videos)} 个目标视频")
            
            if len(results) < 50:
                break
    
    # 按发布时间排序
    all_videos.sort(key=lambda x: x["pubdate"], reverse=True)
    
    return all_videos

def get_all_videos_comprehensive(mid: int) -> list:
    """综合多种方式获取所有视频"""
    all_videos = []
    seen_bvids = set()
    
    # 方法1: 使用不同的排序方式搜索
    orders = ["pubdate", "totalrank", "click", "danmaku", "stow"]
    keywords = ["星月凌云", "-星月凌云-", "星月写作", "Ai写小说", "番茄小说"]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Accept": "application/json",
        "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000",
    }
    
    for order in orders:
        for keyword in keywords:
            for page in range(1, 6):  # 每关键词每排序搜5页
                time.sleep(0.3)
                
                params = urllib.parse.urlencode({
                    "keyword": keyword,
                    "page": page,
                    "pagesize": 50,
                    "search_type": "video",
                    "order": order,
                })
                url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
                
                try:
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                except Exception as e:
                    continue
                
                if data.get("code") != 0:
                    continue
                
                results = data.get("data", {}).get("result", [])
                if not results:
                    break
                
                for item in results:
                    item_mid = item.get("mid")
                    if item_mid == mid:
                        bvid = item.get("bvid", "")
                        if bvid in seen_bvids:
                            continue
                        
                        seen_bvids.add(bvid)
                        all_videos.append({
                            "bvid": bvid,
                            "url": f"https://www.bilibili.com/video/{bvid}",
                            "title": item.get("title", "").replace('<em class="keyword">', "").replace('</em>', ""),
                            "author": item.get("author"),
                            "play": item.get("play"),
                            "danmaku": item.get("video_review"),
                            "favorites": item.get("favorites"),
                            "like": item.get("like"),
                            "pubdate": item.get("pubdate"),
                            "duration": item.get("duration"),
                        })
                
                if len(results) < 50:
                    break
    
    # 按发布时间排序
    all_videos.sort(key=lambda x: x["pubdate"], reverse=True)
    return all_videos

if __name__ == "__main__":
    mid = 382179999
    
    print(f"开始获取 UP主 {mid} 的所有视频...")
    videos = get_all_videos_comprehensive(mid)
    
    print(f"\n共获取 {len(videos)} 个视频")
    
    # 保存到文件
    output_file = "/workspace/xingyue_videos.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "mid": mid,
            "total": len(videos),
            "videos": videos
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n视频列表已保存到: {output_file}")
    
    # 只输出视频链接
    print("\n视频链接列表:")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
        print(f"   {video['url']}")
        print()
