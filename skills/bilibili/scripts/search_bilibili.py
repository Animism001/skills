#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import random

# 搜索B站视频
def search_bilibili_videos(keyword, page=1, pagesize=20):
    """
    搜索B站视频
    keyword: 搜索关键词
    page: 页码
    pagesize: 每页结果数
    """
    # 构建搜索URL
    params = urllib.parse.urlencode({
        "keyword": keyword,
        "page": page,
        "pagesize": pagesize,
        "search_type": "video"
    })
    url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
    
    # 随机用户代理
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://www.bilibili.com",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    
    try:
        # 发送请求
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        # 处理响应
        if data.get("code") != 0:
            return {"error": data.get("message", "搜索失败")}
        
        results = data.get("data", {}).get("result", [])
        videos = []
        
        for item in results:
            video = {
                "title": item.get("title", "").replace('<em class="keyword">', "").replace('</em>', ""),
                "url": f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                "up": item.get("author", ""),
                "play": item.get("play", 0),
                "pubdate": item.get("pubdate", 0)
            }
            videos.append(video)
        
        return {"videos": videos, "total": len(videos)}
        
    except Exception as e:
        return {"error": str(e)}

# 主函数
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python search_bilibili.py <关键词>")
        sys.exit(1)
    
    keyword = sys.argv[1]
    result = search_bilibili_videos(keyword)
    
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print(f"搜索结果 ({result['total']}个视频):")
        for i, video in enumerate(result['videos'], 1):
            print(f"\n{i}. 标题：{video['title']}")
            print(f"   链接：{video['url']}")
            print(f"   UP主：{video['up']}")
            print(f"   播放量：{video['play']}")
            print(f"   发布时间：{video['pubdate']}")
