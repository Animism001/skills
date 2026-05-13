#!/usr/bin/env python3
import requests
import time

test_bv_ids = [
    "BV1GJ411x7h7",
    "BV1Ux411w1iK",
    "BV1xxx1y1q7L"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

def get_subtitle(bv_id):
    print(f"\n{'='*60}")
    print(f"测试视频: {bv_id}")
    print('='*60)

    try:
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        response = requests.get(api_url, headers=headers, timeout=10)
        video_info = response.json()

        if video_info["code"] == 0:
            title = video_info["data"]["title"]
            aid = video_info["data"]["aid"]
            cid = video_info["data"]["pages"][0]["cid"]

            print(f"标题: {title[:50]}...")
            print(f"aid: {aid}, cid: {cid}")

            subtitle_api = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
            subtitle_response = requests.get(subtitle_api, headers=headers, timeout=10)
            subtitle_data = subtitle_response.json()

            if subtitle_data["code"] == 0 and subtitle_data["data"]["subtitle"]["subtitles"]:
                subtitles = subtitle_data["data"]["subtitle"]["subtitles"]
                print(f"✅ 找到 {len(subtitles)} 个字幕!")

                for i, sub in enumerate(subtitles):
                    lan_doc = sub.get('lan_doc', '未知')
                    subtitle_url = sub.get("subtitle_url", "")
                    if not subtitle_url.startswith("http"):
                        subtitle_url = "https:" + subtitle_url

                    print(f"  字幕{i+1}: {lan_doc}")

                    subtitle_content = requests.get(subtitle_url, headers=headers, timeout=10).json()
                    full_text = [item.get("content", "") for item in subtitle_content.get("body", [])]
                    full_subtitle = "\n".join(full_text)

                    print(f"\n# {title}\n")
                    print(full_subtitle[:2000])
                    if len(full_subtitle) > 2000:
                        print(f"\n... (共 {len(full_text)} 条)")
                    return True
            else:
                print("❌ 该视频没有字幕")
        else:
            print(f"❌ 获取视频失败: {video_info.get('message')}")
    except Exception as e:
        print(f"❌ 错误: {e}")

    return False

for bv_id in test_bv_ids:
    if get_subtitle(bv_id):
        break
    time.sleep(1)
