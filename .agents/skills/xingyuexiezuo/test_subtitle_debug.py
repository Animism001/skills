#!/usr/bin/env python3
import requests
import json

bv_id = "BV17xynBwE4b"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

try:
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    response = requests.get(api_url, headers=headers, timeout=10)
    video_info = response.json()

    if video_info["code"] == 0:
        title = video_info["data"]["title"]
        aid = video_info["data"]["aid"]
        cid = video_info["data"]["pages"][0]["cid"]

        print(f"视频标题: {title}")
        print(f"视频ID (aid): {aid}")
        print(f"分P ID (cid): {cid}")
        print("-" * 50)

        subtitle_api = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
        print(f"字幕API: {subtitle_api}")

        subtitle_response = requests.get(subtitle_api, headers=headers, timeout=10)
        subtitle_data = subtitle_response.json()

        print(f"\n字幕API返回:")
        print(f"  code: {subtitle_data.get('code')}")
        print(f"  message: {subtitle_data.get('message')}")

        if subtitle_data.get("data") and subtitle_data["data"].get("subtitle"):
            subtitles = subtitle_data["data"]["subtitle"].get("subtitles", [])
            print(f"  字幕数量: {len(subtitles)}")

            if subtitles:
                for i, sub in enumerate(subtitles[:3]):
                    print(f"\n字幕 {i+1}:")
                    print(f"  原始数据: {json.dumps(sub, indent=2, ensure_ascii=False)}")
            else:
                print("  subtitles 数组为空")
        else:
            print(f"  subtitle_data 结构: {json.dumps(subtitle_data.get('data'), indent=2, ensure_ascii=False)[:500]}")
    else:
        print(f"无法获取视频信息: {video_info.get('message', '未知错误')}")
except Exception as e:
    import traceback
    print(f"获取视频字幕失败: {e}")
    traceback.print_exc()
