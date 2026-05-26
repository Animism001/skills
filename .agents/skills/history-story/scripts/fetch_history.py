#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch_dayinhistory(month, day):
    url = f"https://api.dayinhistory.com/v1/events/{month}/{day}/"
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
                    "month": month,
                    "day": day,
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
                if len(parts) == 2:
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


def main():
    parser = argparse.ArgumentParser(description="Fetch 'today in history' events")
    parser.add_argument("--month", type=int, default=None)
    parser.add_argument("--day", type=int, default=None)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    now = datetime.now()
    month = args.month or now.month
    day = args.day or now.day

    month_name = datetime(2000, month, 1).strftime("%B").lower()

    all_events = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(fetch_dayinhistory, month_name, day),
            executor.submit(fetch_jkapi),
        ]
        for future in as_completed(futures):
            try:
                all_events.extend(future.result())
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)

    all_events = deduplicate(all_events)

    all_events.sort(key=lambda e: (int(e["year"]) if e["year"].isdigit() else 0))

    output = json.dumps({
        "date": f"{month}-{day}",
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
