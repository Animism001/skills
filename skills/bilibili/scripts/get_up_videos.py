#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import random
import time
import os
import gzip
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anti_crawler import get_anti_crawler

# 搜索UP主
def search_up(up_name):
    """
    搜索UP主
    up_name: UP主名称
    """
    anti_crawler = get_anti_crawler()
    
    params = urllib.parse.urlencode({
        "keyword": up_name,
        "search_type": "bili_user",
        "page": 1,
        "pagesize": 50
    })
    url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
    
    headers = anti_crawler.get_complete_headers(
        referer="https://www.bilibili.com",
        is_json=True
    )
    
    try:
        # 随机延迟
        anti_crawler.random_delay()
        
        resp = anti_crawler.make_request(url, headers=headers)
        
        # 处理gzip压缩
        content = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        
        data = json.loads(content.decode("utf-8"))
        
        if data.get("code") != 0:
            return {"error": data.get("message", "搜索失败")}
        
        results = data.get("data", {}).get("result", [])
        if not results:
            return {"error": "未找到该UP主"}
        
        # 找到匹配的UP主
        for item in results:
            if item.get("uname", "").strip() == up_name.strip():
                return {
                    "mid": item.get("mid"),
                    "name": item.get("uname"),
                    "fans": item.get("fans")
                }
        
        # 返回第一个结果
        return {
            "mid": results[0].get("mid"),
            "name": results[0].get("uname"),
            "fans": results[0].get("fans")
        }
        
    except Exception as e:
        return {"error": str(e)}

# 获取UP主的视频
def get_up_videos(mid, page=1, pagesize=50):
    """
    获取UP主的视频
    mid: UP主的mid
    page: 页码
    pagesize: 每页结果数
    """
    anti_crawler = get_anti_crawler()
    
    params = urllib.parse.urlencode({
        "mid": mid,
        "ps": pagesize,
        "pn": page,
        "tid": 0,
        "keyword": "",
        "order": "pubdate"
    })
    url = f"https://api.bilibili.com/x/space/wbi/arc/search?{params}"
    
    headers = anti_crawler.get_complete_headers(
        referer=f"https://space.bilibili.com/{mid}",
        is_json=True
    )
    
    try:
        # 随机延迟
        anti_crawler.random_delay()
        
        resp = anti_crawler.make_request(url, headers=headers)
        
        # 处理gzip压缩
        content = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        
        data = json.loads(content.decode("utf-8"))
        
        if data.get("code") != 0:
            return {"error": data.get("message", "获取视频失败")}
        
        videos = []
        
        # 处理响应数据
        items = data.get("data", {}).get("list", {}).get("vlist", [])
        for item in items:
            video = {
                "bvid": item.get("bvid"),
                "url": f"https://www.bilibili.com/video/{item.get('bvid')}",
                "title": item.get("title"),
                "play": item.get("play"),
                "length": item.get("length"),
                "created": item.get("created")
            }
            videos.append(video)
        
        total = data.get("data", {}).get("page", {}).get("count", 0)
        
        return {
            "videos": videos,
            "total": total,
            "page": page,
            "pagesize": pagesize
        }
        
    except Exception as e:
        return {"error": str(e)}

# 获取UP主的所有视频
def get_all_up_videos(up_name, output_dir="."):
    """
    获取UP主的所有视频
    up_name: UP主名称
    output_dir: 输出目录
    """
    anti_crawler = get_anti_crawler()
    
    # 搜索UP主
    up_info = search_up(up_name)
    if "error" in up_info:
        return {"error": up_info["error"]}
    
    mid = up_info["mid"]
    name = up_info["name"]
    
    print(f"找到UP主: {name} (mid: {mid})")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 文件名
    output_json = os.path.join(output_dir, f"{name}_videos.json")
    output_txt = os.path.join(output_dir, f"{name}_videos.txt")
    
    all_videos = []
    page = 1
    pagesize = 50
    
    while True:
        print(f"获取第 {page} 页视频...")
        result = get_up_videos(mid, page, pagesize)
        
        if "error" in result:
            return {"error": result["error"]}
        
        videos = result.get("videos", [])
        if not videos:
            break
        
        all_videos.extend(videos)
        
        # 检查是否还有更多视频
        if len(all_videos) >= result.get("total", 0):
            break
        
        page += 1
        
        # 每3页进行一次长延迟
        if page % 3 == 0:
            print("进行长延迟，避免触发风控...")
            anti_crawler.long_delay(10, 15)
    
    # 保存JSON文件
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "mid": mid,
            "name": name,
            "total": len(all_videos),
            "videos": all_videos
        }, f, ensure_ascii=False, indent=2)
    
    # 保存文本文件
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(f"B站UP主\"{name}\"完整视频链接列表（共{len(all_videos)}个视频）\n\n")
        
        for i, video in enumerate(all_videos, 1):
            title = video.get("title", "")
            url = video.get("url", "")
            f.write(f"{i}. {title}\n{url}\n\n")
    
    return {
        "name": name,
        "mid": mid,
        "total": len(all_videos),
        "json_path": output_json,
        "txt_path": output_txt
    }

# 主函数
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python get_up_videos.py <UP主名称> [输出目录]")
        sys.exit(1)
    
    up_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    result = get_all_up_videos(up_name, output_dir)
    
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print(f"\n已获取UP主 \"{result['name']}\" 的 {result['total']} 个视频")
        print(f"视频链接已保存到:")
        print(f"- JSON文件: {result['json_path']}")
        print(f"- 文本文件: {result['txt_path']}")
