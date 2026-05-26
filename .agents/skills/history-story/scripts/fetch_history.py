#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_dayinhistory(month, day):
    month_name = datetime(2000, month, 1).strftime("%B").lower()
    url = f"https://api.dayinhistory.com/v1/events/{month_name}/{day}/"
    events = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HistoryStorySkill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                events.append({
                    "source": "dayinhistory",
                    "year": str(item.get("year", "")),
                    "title": item.get("text", item.get("title", "")),
                    "detail": item.get("description", item.get("content", "")),
                    "month": f"{month:02d}",
                    "day": f"{day:02d}",
                })
    except Exception as e:
        print(f"[dayinhistory] fetch error: {e}", file=sys.stderr)
    return events


def fetch_jkapi():
    url = "https://jkapi.com/api/history"
    events = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HistoryStorySkill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("utf-8")
            for line in text.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(None, 1)
                if len(parts) == 2 and parts[0].isdigit():
                    events.append({
                        "source": "jkapi",
                        "year": parts[0],
                        "title": parts[1],
                        "detail": "",
                        "month": "",
                        "day": "",
                    })
    except Exception as e:
        print(f"[jkapi] fetch error: {e}", file=sys.stderr)
    return events


def deduplicate(events):
    seen = set()
    result = []
    for e in events:
        key = (e["year"], e["title"][:20])
        if key not in seen:
            seen.add(key)
            result.append(e)
    return result


def save_events_md(events, month, day, base_dir="dayinhistory"):
    mm = f"{month:02d}"
    dd = f"{day:02d}"
    dir_path = os.path.join(base_dir, mm, dd)
    os.makedirs(dir_path, exist_ok=True)
    filepath = os.path.join(dir_path, "events.md")

    lines = [f"# 历史上的今天 {month}月{day}日\n"]
    lines.append("## 事件列表\n")
    lines.append("| # | 年份 | 事件 | 来源 |")
    lines.append("|---|------|------|------|")
    for i, e in enumerate(events, 1):
        lines.append(f"| {i} | {e['year']} | {e['title']} | {e['source']} |")
    lines.append("")
    lines.append(f"共 {len(events)} 个事件。")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Events saved to {filepath}", file=sys.stderr)
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Fetch 'today in history' events")
    parser.add_argument("--month", type=int, default=None)
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--save-dir", type=str, default="dayinhistory",
                        help="Base directory to save events.md (default: dayinhistory)")
    args = parser.parse_args()

    now = datetime.now()
    month = args.month or now.month
    day = args.day or now.day

    all_events = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(fetch_dayinhistory, month, day),
            executor.submit(fetch_jkapi),
        ]
        for future in as_completed(futures):
            try:
                all_events.extend(future.result())
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

    all_events = deduplicate(all_events)
    all_events.sort(key=lambda e: (int(e["year"]) if e["year"].isdigit() else 0))

    save_events_md(all_events, month, day, base_dir=args.save_dir)

    output = json.dumps({
        "date": f"{month:02d}-{day:02d}",
        "count": len(all_events),
        "events": all_events,
    }, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
