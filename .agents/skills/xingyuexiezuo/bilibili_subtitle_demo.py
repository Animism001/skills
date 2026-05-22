#!/usr/bin/env python3
"""
B站视频字幕获取脚本
基于你提供的方法实现
"""

import requests
import json

def get_bilibili_subtitle(bv_id):
    """
    获取B站视频字幕的完整流程

    第一步：获取视频信息 (API: /x/web-interface/view)
    第二步：获取字幕列表 (API: /x/player/v2)
    第三步：下载并解析字幕 (字幕文件是JSON格式)
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }

    print("=" * 60)
    print("B站字幕获取演示")
    print("=" * 60)

    # ===== 第一步：获取视频基本信息 =====
    print("\n📺 第一步：获取视频信息")
    print("-" * 40)

    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        video_info = response.json()

        if video_info["code"] == 0:
            title = video_info["data"]["title"]
            aid = video_info["data"]["aid"]
            cid = video_info["data"]["pages"][0]["cid"]

            print(f"  视频标题: {title}")
            print(f"  视频ID (aid): {aid}")
            print(f"  分P ID (cid): {cid}")
        else:
            print(f"  ❌ 获取视频失败: {video_info.get('message', '未知错误')}")
            return None

    except Exception as e:
        print(f"  ❌ 请求失败: {e}")
        return None

    # ===== 第二步：获取字幕列表 =====
    print("\n📝 第二步：获取字幕列表")
    print("-" * 40)

    subtitle_api = f"https://api.bilibili.com/x/player/v2?aid={aid}&cid={cid}"
    print(f"  API: {subtitle_api}")

    try:
        subtitle_response = requests.get(subtitle_api, headers=headers, timeout=10)
        subtitle_data = subtitle_response.json()

        if subtitle_data["code"] == 0:
            subtitles = subtitle_data["data"]["subtitle"]["subtitles"]

            if subtitles:
                print(f"  ✅ 找到 {len(subtitles)} 个字幕!")

                for i, sub in enumerate(subtitles):
                    print(f"\n  字幕 {i+1}:")
                    print(f"    语言: {sub.get('lan_doc', '未知')}")
                    print(f"    字幕URL: {sub.get('subtitle_url', '')[:60]}...")

                    # ===== 第三步：下载并解析字幕 =====
                    print("\n  📥 第三步：下载字幕内容")

                    subtitle_url = sub.get("subtitle_url", "")
                    if not subtitle_url.startswith("http"):
                        subtitle_url = "https:" + subtitle_url

                    subtitle_content = requests.get(subtitle_url, headers=headers, timeout=10).json()

                    # 字幕JSON格式说明
                    print(f"    字幕格式: JSON")
                    print(f"    字幕条数: {len(subtitle_content.get('body', []))}")

                    # 提取文本
                    full_text = []
                    for item in subtitle_content["body"]:
                        full_text.append(item["content"])

                    full_subtitle = "\n".join(full_text)

                    print(f"\n{'='*60}")
                    print(f"视频标题: {title}")
                    print("=" * 60)
                    print(full_subtitle[:2000])
                    if len(full_subtitle) > 2000:
                        print(f"\n... (共 {len(full_text)} 条字幕)")
                    print("=" * 60)

                    return {
                        "title": title,
                        "subtitle": full_subtitle,
                        "count": len(full_text)
                    }
            else:
                print("  ❌ 该视频没有字幕")
                return None
        else:
            print(f"  ❌ 字幕API错误: {subtitle_data.get('message')}")
            return None

    except Exception as e:
        print(f"  ❌ 请求失败: {e}")
        return None

if __name__ == "__main__":
    # 使用示例 BV 号
    bv_id = "BV1pyduBzE69"

    print("\n🎯 测试目标视频:", bv_id)
    result = get_bilibili_subtitle(bv_id)

    if result:
        print(f"\n✅ 成功获取字幕！共 {result['count']} 条")
    else:
        print("\n⚠️  未获取到字幕")
        print("\n说明：")
        print("  1. 该视频可能没有上传字幕")
        print("  2. B站API可能有访问限制")
        print("  3. 字幕获取需要视频本身包含字幕文件")
