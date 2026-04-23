#!/usr/bin/env python3
import json
import time
import random
import urllib.request
import urllib.parse

# 合并所有现有的视频文件
def merge_existing_videos():
    """合并所有现有的视频文件"""
    all_videos = []
    seen_bvids = set()
    
    # 要合并的文件
    files = [
        "/workspace/xingyue_videos.json",
        "/workspace/xingyue_videos_complete.json"
    ]
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            videos = data.get("videos", [])
            for video in videos:
                bvid = video.get("bvid")
                if bvid and bvid not in seen_bvids:
                    seen_bvids.add(bvid)
                    all_videos.append(video)
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
    
    # 按发布时间排序
    def get_pubdate(video):
        return video.get("pubdate", 0) or video.get("created", 0) or 0
    
    all_videos.sort(key=get_pubdate, reverse=True)
    
    print(f"合并后共有 {len(all_videos)} 个视频")
    return all_videos

# 获取剩余的视频
def get_remaining_videos(mid: int, existing_bvids: set, target_count: int) -> list:
    """获取剩余的视频，使用多种搜索策略"""
    missing_videos = []
    seen_bvids = set(existing_bvids)
    
    # 随机用户代理
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    ]
    
    def get_random_headers():
        return {
            "User-Agent": random.choice(user_agents),
            "Referer": f"https://space.bilibili.com/{mid}",
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cookie": "buvid3=openclaw_bilibili_skill_v1; b_nut=1700000000; buvid4=openclaw_bilibili_skill_v1",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://space.bilibili.com",
        }
    
    print(f"开始搜索剩余视频，当前已获取 {len(seen_bvids)} 个，目标 {target_count} 个")
    
    # 尝试不同的搜索关键词和排序方式
    search_keywords = [
        "星月凌云",
        "-星月凌云-", 
        "星月写作",
        "Ai写小说",
        "番茄小说",
        "AI写作",
        "网文",
        "小说写作",
        "星月AI",
        "AI网文"
    ]
    
    orders = ["pubdate", "totalrank", "click", "danmaku", "stow"]
    
    for keyword in search_keywords:
        for order in orders:
            for page in range(1, 6):  # 每关键词每排序搜5页
                # 随机延迟 1-3 秒
                delay = random.uniform(1, 3)
                print(f"\n搜索关键词: {keyword}, 排序: {order}, 第 {page} 页，延迟 {delay:.2f} 秒...")
                time.sleep(delay)
                
                params = urllib.parse.urlencode({
                    "keyword": keyword,
                    "page": page,
                    "pagesize": 50,
                    "search_type": "video",
                    "order": order,
                })
                url = f"https://api.bilibili.com/x/web-interface/search/type?{params}"
                
                try:
                    headers = get_random_headers()
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                except Exception as e:
                    print(f"  请求失败: {e}")
                    continue
                
                if data.get("code") != 0:
                    print(f"  API错误: {data.get('message')}")
                    continue
                
                results = data.get("data", {}).get("result", [])
                if not results:
                    print("  无更多搜索结果")
                    break
                
                new_videos = 0
                for item in results:
                    item_mid = item.get("mid")
                    if item_mid == mid:
                        bvid = item.get("bvid", "")
                        if bvid in seen_bvids:
                            continue
                        
                        seen_bvids.add(bvid)
                        missing_videos.append({
                            "bvid": bvid,
                            "url": f"https://www.bilibili.com/video/{bvid}",
                            "title": item.get("title", "").replace('<em class="keyword">', "").replace('</em>', ""),
                            "play": item.get("play"),
                            "danmaku": item.get("video_review"),
                            "duration": item.get("duration"),
                            "pubdate": item.get("pubdate"),
                        })
                        new_videos += 1
                        print(f"  发现新视频: {item.get('title', '').replace('<em class="keyword">', '').replace('</em>', '')}")
                
                print(f"  本页发现 {new_videos} 个新视频")
                
                current_total = len(existing_bvids) + len(missing_videos)
                print(f"  当前累计: {current_total} 个视频")
                
                if current_total >= target_count:
                    print(f"\n✅ 成功达到目标数量: {current_total} 个视频！")
                    return missing_videos
    
    print(f"\n最终发现 {len(missing_videos)} 个新视频")
    return missing_videos

# 主函数
def main():
    mid = 382179999
    target_count = 155
    
    # 合并现有的视频
    existing_videos = merge_existing_videos()
    existing_bvids = set(video.get("bvid") for video in existing_videos)
    
    print(f"开始获取剩余的视频（目标：{target_count}个视频）...")
    
    # 执行获取
    missing = get_remaining_videos(mid, existing_bvids, target_count)
    
    # 合并所有视频
    all_videos = existing_videos + missing
    
    # 去重
    seen_bvids = set()
    unique_videos = []
    for video in all_videos:
        bvid = video.get("bvid")
        if bvid not in seen_bvids:
            seen_bvids.add(bvid)
            unique_videos.append(video)
    
    # 按发布时间排序
    def get_pubdate(video):
        return video.get("pubdate", 0) or video.get("created", 0) or 0
    
    unique_videos.sort(key=get_pubdate, reverse=True)
    
    final_count = len(unique_videos)
    print(f"\n最终获取 {final_count} 个视频")
    
    # 保存到文件
    output_json = "/workspace/xingyue_videos_final.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({
            "mid": mid,
            "total": final_count,
            "target": target_count,
            "videos": unique_videos
        }, f, ensure_ascii=False, indent=2)
    
    # 生成链接文件
    output_txt = "/workspace/xingyue_videos_final_links.txt"
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(f"B站UP主\"-星月凌云-\"完整视频链接列表（共{final_count}个视频，目标{target_count}个）\n\n")
        
        for i, video in enumerate(unique_videos, 1):
            title = video.get("title", "")
            url = video.get("url", "")
            f.write(f"{i}. {title}\n{url}\n\n")
        
        f.write(f"\n---\n\n以上列表生成于2026-04-23，数据来源：B站公开API\n")
        f.write(f"目标获取数量：{target_count}个\n")
        f.write(f"实际获取数量：{final_count}个\n")
        if final_count >= target_count:
            f.write("状态：✅ 成功达到目标数量\n")
        else:
            f.write(f"状态：❌ 还差 {target_count - final_count} 个视频\n")
    
    print(f"\n最终视频列表已保存到:")
    print(f"- JSON文件: {output_json}")
    print(f"- 链接文件: {output_txt}")

if __name__ == "__main__":
    main()
