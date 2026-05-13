#!/usr/bin/env python3
import requests

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
        subtitle_response = requests.get(subtitle_api, headers=headers, timeout=10)
        subtitle_data = subtitle_response.json()

        if subtitle_data["code"] == 0 and subtitle_data["data"]["subtitle"]["subtitles"]:
            subtitles = subtitle_data["data"]["subtitle"]["subtitles"]
            print(f"找到 {len(subtitles)} 个字幕:")

            for i, sub in enumerate(subtitles):
                print(f"\n字幕 {i+1}:")
                print(f"  语言: {sub.get('lan_doc', '未知')}")
                print(f"  链接: {sub.get('subtitle_url', '')[:80]}...")

                subtitle_url = sub.get("subtitle_url", "")
                if not subtitle_url.startswith("http"):
                    subtitle_url = "https:" + subtitle_url

                subtitle_content = requests.get(subtitle_url, headers=headers, timeout=10).json()

                full_text = []
                for item in subtitle_content.get("body", []):
                    full_text.append(item.get("content", ""))

                full_subtitle = "\n".join(full_text)

                print(f"\n# {title}\n")
                print(full_subtitle[:2000])
                if len(full_subtitle) > 2000:
                    print(f"\n... (共 {len(full_text)} 行，约 {len(full_subtitle)} 字符)")
        else:
            print("该视频没有字幕或无法获取字幕")
    else:
        print(f"无法获取视频信息: {video_info.get('message', '未知错误')}")
except Exception as e:
    print(f"获取视频字幕失败: {e}")
