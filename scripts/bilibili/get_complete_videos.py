#!/usr/bin/env python3
import sys
import json
import time
import urllib.request
import urllib.parse

def get_all_user_videos(mid: int) -> list:
    """获取UP主的所有视频"""
    all_videos = []
    seen_bvids = set()
    
    # 方法1: 空间视频列表API
    def get_space_videos():
        nonlocal all_videos, seen_bvids
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": f"https://space.bilibili.com/{mid}",
            "Accept": "application/json",
            "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000; buvid4=openclaw_bilibili_skill_v1",
        }
        
        page = 1
        while True:
            time.sleep(1)
            url = f"https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&pn={page}&order=pubdate"
            
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                print(f"空间API请求失败: {e}")
                break
            
            if data.get("code") != 0:
                print(f"空间API错误: {data.get('message')}")
                break
            
            vlist = data.get("data", {}).get("list", {}).get("vlist", [])
            if not vlist:
                break
            
            print(f"空间API第 {page} 页获取了 {len(vlist)} 个视频")
            
            for item in vlist:
                bvid = item.get("bvid", "")
                if bvid in seen_bvids:
                    continue
                
                seen_bvids.add(bvid)
                all_videos.append({
                    "bvid": bvid,
                    "url": f"https://www.bilibili.com/video/{bvid}",
                    "title": item.get("title", ""),
                    "play": item.get("play"),
                    "length": item.get("length"),
                    "created": item.get("created"),
                })
            
            total = data.get("data", {}).get("page", {}).get("count", 0)
            if len(all_videos) >= total:
                print(f"空间API已获取 {len(all_videos)}/{total} 个视频")
                break
            
            page += 1
    
    # 方法2: 搜索API补充
    def get_search_videos():
        nonlocal all_videos, seen_bvids
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.bilibili.com",
            "Accept": "application/json",
            "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000",
        }
        
        keywords = ["星月凌云", "-星月凌云-", "星月写作", "Ai写小说", "番茄小说", "AI写作", "网文", "小说写作"]
        orders = ["pubdate", "totalrank", "click"]
        
        for keyword in keywords:
            for order in orders:
                page = 1
                while page <= 5:
                    time.sleep(0.5)
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
                        break
                    
                    if data.get("code") != 0:
                        break
                    
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
                                "play": item.get("play"),
                                "danmaku": item.get("video_review"),
                                "duration": item.get("duration"),
                                "pubdate": item.get("pubdate"),
                            })
                    
                    page += 1
    
    # 执行方法1
    print("开始使用空间API获取视频...")
    get_space_videos()
    
    # 执行方法2
    print("\n开始使用搜索API补充视频...")
    get_search_videos()
    
    # 去重并按发布时间排序
    unique_videos = []
    seen = set()
    for video in all_videos:
        bvid = video.get("bvid")
        if bvid not in seen:
            seen.add(bvid)
            unique_videos.append(video)
    
    # 按发布时间排序
    unique_videos.sort(key=lambda x: x.get("created", 0) or x.get("pubdate", 0), reverse=True)
    
    return unique_videos

if __name__ == "__main__":
    mid = 382179999
    
    print(f"开始获取 UP主 {mid} 的完整视频列表...")
    videos = get_all_user_videos(mid)
    
    print(f"\n共获取 {len(videos)} 个视频")
    
    # 保存到文件
    output_json = "/workspace/xingyue_videos_complete.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "mid": mid,
            "total": len(videos),
            "videos": videos
        }, f, ensure_ascii=False, indent=2)
    
    # 生成链接文件
    output_txt = "/workspace/xingyue_videos_complete_links.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(f"B站UP主\"-星月凌云-\"完整视频链接列表（共{len(videos)}个视频）\n\n")
        for i, video in enumerate(videos, 1):
            title = video.get("title", "")
            url = video.get("url", "")
            f.write(f"{i}. {title}\n{url}\n\n")
        f.write("\n---\n\n以上列表生成于2026-04-22，数据来源：B站公开API\n")
    
    print(f"\n完整视频列表已保存到:")
    print(f"- JSON文件: {output_json}")
    print(f"- 链接文件: {output_txt}")
