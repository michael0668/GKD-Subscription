#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gkd 快照解析器：解压 zip 快照包并分析节点树，为生成 gkd 规则提供关键信息。

用法:
    python parse_snapshot.py <snapshot.zip|snapshot_dir|snapshot.json> [--full]

功能:
    1. 解压 zip（或直接读取已解压目录 / 单个 json 文件）
    2. 解析快照 JSON，提取 appId / activityId / 应用名 / 版本
    3. 打印完整节点树（id / pid / depth / name / vid / id / clickable / bounds）
    4. 高亮疑似「关闭/跳过/取消」按钮的节点（vid 或 id 含 close/skip/cancel/x/关闭等关键词）
    5. --full 时额外输出每个节点的全部属性（desc/text 等）

输出说明:
    规则生成时优先参考 [CLOSE CANDIDATES] 段落，确认目标节点后据此编写选择器。
"""
import sys
import os
import json
import zipfile
import tempfile
import shutil

CLOSE_KEYWORDS = [
    "close", "skip", "cancel", "dismiss", "exit", "quit", "x", "关闭", "跳过",
    "取消", "忽略", "退出", "我知道了", "知道了", "暂不", "下次再说", "同意",
]

def find_snapshot_json(path):
    """从 zip / 目录 / 单文件 中定位快照 json 文件，返回 json 文件路径列表。"""
    path = os.path.abspath(path)
    results = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".json"):
                    results.append(os.path.join(root, f))
    elif path.endswith(".zip"):
        tmp = tempfile.mkdtemp(prefix="gkd_snap_")
        with zipfile.ZipFile(path) as z:
            z.extractall(tmp)
        results = find_snapshot_json(tmp)
    elif path.endswith(".json"):
        results.append(path)
    return results

def is_snapshot(obj):
    return isinstance(obj, dict) and "nodes" in obj and "appId" in obj

def describe_node(n):
    a = n.get("attr", {})
    return {
        "id": n.get("id"),
        "pid": n.get("pid"),
        "depth": a.get("depth"),
        "name": a.get("name"),
        "vid": a.get("vid"),
        "aid": a.get("id"),
        "text": a.get("text"),
        "desc": a.get("desc"),
        "clickable": a.get("clickable"),
        "bounds": (a.get("left"), a.get("top"), a.get("right"), a.get("bottom")),
    }

def keyword_hit(s):
    if not s:
        return False
    low = s.lower()
    return any(k in low for k in CLOSE_KEYWORDS)

def main():
    if len(sys.argv) < 2:
        print("用法: python parse_snapshot.py <snapshot.zip|dir|json> [--full]")
        sys.exit(1)
    src = sys.argv[1]
    full = "--full" in sys.argv

    json_files = find_snapshot_json(src)
    if not json_files:
        print("错误：未找到快照 JSON 文件。请确认路径是 gkd 快照 zip / 解压目录 / json。")
        sys.exit(1)

    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"跳过 {jf}：解析失败 {e}")
            continue
        if not is_snapshot(data):
            print(f"跳过 {jf}：不是有效的 gkd 快照（缺少 nodes/appId）。")
            continue

        print("=" * 70)
        print(f"快照文件: {os.path.basename(jf)}")
        print(f"appId     : {data.get('appId')}")
        print(f"activityId: {data.get('activityId')}")
        ai = data.get("appInfo", {})
        print(f"应用名    : {ai.get('name')}  版本 {ai.get('versionName')} (code {ai.get('versionCode')})")
        print(f"屏幕尺寸  : {data.get('screenWidth')} x {data.get('screenHeight')}")
        nodes = data.get("nodes", [])
        print(f"节点总数  : {len(nodes)}")
        print("-" * 70)
        print("节点树 (depth 缩进):")
        for n in nodes:
            d = describe_node(n)
            ind = "  " * (d["depth"] or 0)
            flag = ""
            if d["clickable"]:
                flag += " [可点击]"
            if keyword_hit(d["vid"]) or keyword_hit(d["aid"]) or keyword_hit(d["text"]) or keyword_hit(d["desc"]):
                flag += " [★疑似目标]"
            extra = ""
            if d["text"] or d["desc"]:
                extra = f" text={d['text']!r} desc={d['desc']!r}"
            print(f"{ind}[node {d['id']} pid={d['pid']}] {d['name']} vid={d['vid']} id={d['aid']}{extra}{flag}")
            if full:
                print(f"{ind}    bounds={d['bounds']} clickable={d['clickable']}")
        print()

    # 汇总疑似关闭按钮
    print("=" * 70)
    print("[CLOSE CANDIDATES] 疑似关闭/跳过按钮节点（供编写选择器参考）:")
    found = False
    for jf in json_files:
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if not is_snapshot(data):
            continue
        for n in data.get("nodes", []):
            d = describe_node(n)
            if keyword_hit(d["vid"]) or keyword_hit(d["aid"]) or keyword_hit(d["text"]) or keyword_hit(d["desc"]):
                found = True
                print(f"  vid={d['vid']}  id={d['aid']}  name={d['name']}  clickable={d['clickable']}  text={d['text']!r} desc={d['desc']!r}")
    if not found:
        print("  （未命中关键词，请根据节点树人工判断目标按钮）")

if __name__ == "__main__":
    main()
