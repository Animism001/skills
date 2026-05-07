#!/usr/bin/env python3
import requests
import json
import urllib.parse

# 测试B站搜索API
keyword = "起点编辑 星河"
params = urllib.parse.urlencode({
    "keyword": keyword,
    "page": 1,
    "pagesize": 20,
    "search_type": "video"
})
url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://search.bilibili.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest"
}

print(f"测试搜索: {keyword}")
print(f"URL: {url}")

try:
    response = requests.get(url, headers=headers, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容长度: {len(response.content)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"JSON数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"响应内容: {response.text[:500]}...")
    else:
        print(f"错误响应: {response.text}")
        
except Exception as e:
    print(f"请求错误: {e}")
