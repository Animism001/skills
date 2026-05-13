#!/usr/bin/env python3
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

test_videos = [
    "BV1GJ411x7h7",  # Rick Astley - Never Gonna Give You Up
    "BV1sL411p7uK",  # 3Blue1Brown
    "BV1uT411B7Df",  # 计算机科学
    "BV1ru411s7fA",  # TED演讲
]

def try_get_subtitle(bv_id):
    print(f"\n测试: {bv_id}")

    try:
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        response = requests.get(api_url, headers=headers, timeout=10)
        video_info = response.json()

        if video_info["code"] == 0:
            title = video_info["data"]["title"]
            aid = video_info["data"]["aid"]
            cid = video_info["data"]["pages"][0]["cid"]

            print(f"  标题: {title[:40]}...")

            subtitle_api = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
            subtitle_response = requests.get(subtitle_api, headers=headers, timeout=10)
            subtitle_data = subtitle_response.json()

            if subtitle_data["code"] == 0:
                subtitles = subtitle_data.get("data", {}).get("subtitle", {}).get("subtitles", [])
                if subtitles:
                    print(f"  ✅ 找到 {len(subtitles)} 个字幕!")

                    for sub in subtitles:
                        lan_doc = sub.get('lan_doc', '未知')
                        print(f"    - {lan_doc}")

                        subtitle_url = sub.get("subtitle_url", "")
                        if not subtitle_url.startswith("http"):
                            subtitle_url = "https:" + subtitle_url

                        subtitle_content = requests.get(subtitle_url, headers=headers, timeout=10).json()
                        full_text = [item.get("content", "") for item in subtitle_content.get("body", [])]
                        full_subtitle = "\n".join(full_text)

                        print(f"\n{'='*60}")
                        print(f"视频: {title}")
                        print("=" * 60)
                        print(full_subtitle[:1500])
                        if len(full_subtitle) > 1500:
                            print(f"\n... (共 {len(full_text)} 条)")
                        print("=" * 60)
                        return True
                    return False
                else:
                    print("  ❌ 无字幕")
            else:
                print(f"  ❌ API错误")
        else:
            print(f"  ❌ 获取失败")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

    return False

for bv_id in test_videos:
    if try_get_subtitle(bv_id):
        break
    time.sleep(1)
