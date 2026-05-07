import json
import subprocess
import time

all_videos = []

# 遍历10页视频数据
for page in range(1, 11):
    print(f"Fetching page {page}...")
    # 调用bilibili-search技能获取视频数据
    result = subprocess.run([
        "python3", "scripts/bilibili.py",
        f'{{"action":"search","query":"给星大录","count":20,"page":{page},"order":"pubdate"}}'
    ], cwd="/workspace/skills/bilibili-search", capture_output=True, text=True)
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            if "results" in data:
                all_videos.extend(data["results"])
                print(f"Added {len(data['results'])} videos from page {page}")
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from page {page}")
    else:
        print(f"Failed to fetch page {page}: {result.stderr}")
    
    # 添加延迟避免被封
    time.sleep(2)

# 保存所有视频信息到json文件
output_file = "/workspace/star_river_videos/all_videos.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"videos": all_videos}, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(all_videos)} videos to {output_file}")
print(f"Total videos: {len(all_videos)}")