#!/usr/bin/env python3
import json
import urllib.parse
import gzip
from io import BytesIO
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anti_crawler import get_anti_crawler

# 搜索B站视频
def search_bilibili_videos(keyword, page=1, pagesize=20):
    """
    搜索B站视频
    keyword: 搜索关键词
    page: 页码
    pagesize: 每页结果数
    """
    # 获取反爬管理器
    anti_crawler = get_anti_crawler()
    
    # 构建搜索URL
    params = urllib.parse.urlencode({
        "keyword": keyword,
        "page": page,
        "pagesize": pagesize,
        "search_type": "video"
    })
    url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
    
    # 随机延迟
    if page == 1:
        anti_crawler.random_delay(1, 3)
    else:
        anti_crawler.random_delay(3, 8)
    
    # 获取完整请求头
    headers = anti_crawler.get_complete_headers(
        referer="https://search.bilibili.com",
        is_json=True
    )
    
    try:
        # 发送请求（使用反爬管理器）
        resp = anti_crawler.make_request(url, headers=headers, max_retries=5, timeout=30)
        
        # 处理响应，支持gzip压缩
        content_encoding = resp.getheader('Content-Encoding')
        content = resp.read()
        print(f"响应状态码: {resp.getcode()}")
        print(f"响应头: {dict(resp.getheaders())}")
        print(f"响应内容长度: {len(content)}")
        
        if content_encoding and 'gzip' in content_encoding:
            buffer = BytesIO(content)
            with gzip.GzipFile(fileobj=buffer) as f:
                content = f.read()
                print(f"解压后内容长度: {len(content)}")
        
        try:
            data = json.loads(content.decode('utf-8'))
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"响应内容: {content[:500]}...")  # 只打印前500个字符
            return {"error": f"JSON解析失败: {str(e)}"}
        
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
