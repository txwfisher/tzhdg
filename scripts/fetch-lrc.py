#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M4A 封面/歌词提取 + Meting API 音乐下载 + 自动生成博客 md

用法:
    # 本地文件模式：处理 M4A 文件
    python fetch-lrc.py <文件或目录>                              # 提取封面和歌词
    python fetch-lrc.py <文件或目录> --md                          # 同时生成 md
    python fetch-lrc.py . --md --server=kugou                     # 换平台

    # 搜索下载模式：直接搜歌名下载（音频+歌词+封面+md）
    python fetch-lrc.py "歌名" ["歌手"] --md                       # 搜索并下载
    python fetch-lrc.py "晴天" "周杰伦" --md                       # 指定歌手
    python fetch-lrc.py "海阔天空" --md --server=kugou --out=./dl  # 换平台+指定目录

    # 自定义
    python fetch-lrc.py . --no-md --audio-base=https://xxx/music/ # 自定义 URL

默认输出目录: ./downloads/
默认 md 输出: src/content/bangumi/music/
默认音频 URL 前缀: https://ph.0824.uk/file/music/

依赖: 已部署的 Meting API, mutagen
"""

import json
import os
import re
import sys
import unicodedata
import urllib.request
from datetime import date

from mutagen import mp4
from mutagen.mp4 import MP4Cover

API_BASE = "https://mu.tsh520.cn/api"
BLOG_CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "content", "bangumi", "music"))
AUDIO_BASE = "https://ph.0824.uk/file/music/"
DEFAULT_OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "downloads"))


# ── utility ──────────────────────────────────────────

def human_size(n):
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return "{:.0f} {}".format(n, u)
        n /= 1024
    return "{:.1f} GB".format(n)


def sanitize_filename(name):
    """只保留各国语言文字和数字，去除所有符号（- . / _ 空格 等）"""
    result = []
    for ch in name:
        cat = unicodedata.category(ch)
        if cat.startswith("L") or cat.startswith("N"):
            result.append(ch)
    return "".join(result)


def download_file(url, filepath, label=""):
    """下载文件带进度条"""
    try:
        with urllib.request.urlopen(url, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            with open(filepath, "wb") as f:
                downloaded = 0
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = downloaded * 100 // total
                        bar_len = 25
                        filled = downloaded * bar_len // total
                        bar = "=" * filled + ">" + " " * (bar_len - filled)
                        print("\r  {} [{:3d}%] {} {}/{}".format(
                            label, pct, bar, human_size(downloaded), human_size(total)), end="")
                print()
        return True
    except Exception as e:
        print("\n  下载失败: {}".format(e))
        if os.path.exists(filepath):
            os.remove(filepath)
        return False


# ── API helpers ───────────────────────────────────────

def search_songs(name, artist="", server="netease"):
    """搜索歌曲，返回全部结果"""
    query = "{} {}".format(name, artist).strip()
    url = "{}?server={}&type=search&id={}".format(
        API_BASE, server, urllib.request.quote(query))
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if isinstance(data, list) else []
    except Exception as e:
        print("  搜索失败: {}".format(e))
        return []


def search_first(name, artist="", server="netease"):
    """搜索歌曲，返回第一首"""
    results = search_songs(name, artist, server)
    return results[0] if results else None


def fetch_lrc(lyric_id, server="netease"):
    """根据 lyric_id 获取 LRC 歌词"""
    url = "{}?server={}&type=song&id={}".format(
        API_BASE, server, urllib.request.quote(str(lyric_id)))
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data if isinstance(data, list) else [data]
            if items and items[0].get("lrc"):
                with urllib.request.urlopen(items[0]["lrc"], timeout=15) as lrc_resp:
                    return lrc_resp.read().decode("utf-8")
    except Exception as e:
        print("  歌词获取失败: {}".format(e))
    return None


def fetch_cover_bytes(pic_url):
    try:
        with urllib.request.urlopen(pic_url, timeout=15) as resp:
            return resp.read()
    except Exception:
        return None


# ── local file helpers ────────────────────────────────

def extract_embedded_cover(filepath):
    try:
        audio = mp4.MP4(filepath)
        covers = audio.tags.get("covr")
        if covers:
            cover = covers[0]
            fmt_map = {MP4Cover.FORMAT_JPEG: "jpg", MP4Cover.FORMAT_PNG: "png"}
            return bytes(cover), fmt_map.get(cover.imageformat, "jpg")
    except Exception:
        pass
    return None, None


def read_audio_tags(filepath):
    try:
        audio = mp4.MP4(filepath)
        tags = dict(audio.tags or {})
        name = str(tags.get("\xa9nam", [""])[0]).strip()
        artist = str(tags.get("\xa9ART", [""])[0]).strip()
        return name, artist
    except Exception:
        return os.path.splitext(os.path.basename(filepath))[0], ""


# ── markdown ──────────────────────────────────────────

def write_markdown(md_path, name, artist, audio_url, lrc_url, cover_url):
    text = """---
title: {name}
category: music
status: 2
image: {cover}
artist: {artist}
audioUrl: {audio}
lrcUrl: {lrc}
score: 0
published: {today}
---

""".format(
        name=name,
        artist=artist,
        cover=cover_url,
        audio=audio_url,
        lrc=lrc_url,
        today=date.today().isoformat(),
    )
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text)


# ── file mode ─────────────────────────────────────────

def process_file(filepath, server="netease", audio_base=None, md_dir=None):
    """处理本地音频文件：封面 + 歌词 + 可选 md"""
    base = os.path.splitext(filepath)[0]
    basename = os.path.basename(filepath)
    slug = os.path.splitext(basename)[0]
    changed = False

    cover_path = base + ".jpg"
    _, cover_filename = os.path.split(cover_path)

    if os.path.exists(cover_path):
        print("  [跳过] 已有封面 {}".format(cover_filename))
    else:
        img_bytes, fmt = extract_embedded_cover(filepath)
        if img_bytes:
            cover_path = base + "." + fmt
            _, cover_filename = os.path.split(cover_path)
            with open(cover_path, "wb") as f:
                f.write(img_bytes)
            print("  [封面:内嵌] {}".format(cover_filename))
            changed = True

    name, artist = read_audio_tags(filepath)
    if not name:
        return changed

    print("  搜索: {} - {}".format(name, artist or "未知"))
    song = search_first(name, artist, server)
    if not song:
        print("  [未找到] {} - {}".format(name, artist))
        return changed

    if not os.path.exists(cover_path) and song.get("pic"):
        img_bytes = fetch_cover_bytes(song["pic"])
        if img_bytes:
            with open(cover_path, "wb") as f:
                f.write(img_bytes)
            print("  [封面:API] {}".format(cover_filename))
            changed = True

    lrc_path = base + ".lrc"
    _, lrc_filename = os.path.split(lrc_path)
    if os.path.exists(lrc_path):
        print("  [跳过] 已有歌词 {}".format(lrc_filename))
    else:
        lyric_id = song.get("lyric_id") or song.get("id")
        lrc = fetch_lrc(lyric_id, server)
        if not lrc and song.get("lrc"):
            try:
                with urllib.request.urlopen(song["lrc"], timeout=15) as resp:
                    lrc = resp.read().decode("utf-8")
            except Exception:
                pass
        if lrc:
            with open(lrc_path, "w", encoding="utf-8") as f:
                f.write(lrc)
            print("  [歌词] {} ({} 字符)".format(lrc_filename, len(lrc)))
            changed = True
        else:
            print("  [无歌词] {}".format(name))

    if audio_base and md_dir is not None:
        audio_base = audio_base.rstrip("/") + "/"
        audio_url = audio_base + basename
        lrc_url = audio_base + slug + ".lrc"
        cover_url = audio_base + os.path.splitext(cover_filename)[0] + ".jpg"
        md_file = sanitize_filename(name) + ".md"
        md_path = os.path.join(md_dir, md_file)
        if os.path.exists(md_path):
            print("  [跳过] 已有 md: {}".format(md_file))
        else:
            write_markdown(md_path, name, artist, audio_url, lrc_url, cover_url)
            print("  [MD] {}".format(md_file))
            changed = True

    return changed


# ── search mode ───────────────────────────────────────

def process_search(name, artist="", server="netease", audio_base=None, md_dir=None, out_dir=None):
    """搜索并下载：音频 + 封面 + 歌词 + md"""
    if out_dir is None:
        out_dir = DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)

    print("搜索: {} - {}".format(name, artist or "任意"))
    results = search_songs(name, artist, server)
    if not results:
        print("未找到结果")
        return False

    print("\n搜索结果:\n")
    for i, item in enumerate(results[:10]):
        t = item.get("title") or item.get("name") or "?"
        a = item.get("author") or item.get("artist") or "?"
        sid = item.get("id", "?")
        print("  [{:2d}] {} - {}  (id: {})".format(i + 1, t, a, sid))

    if len(results) == 1:
        pick = 1
    else:
        try:
            choice = input("\n选择序号 (1-{}, 默认 1): ".format(min(10, len(results)))).strip()
            pick = int(choice) if choice else 1
            if pick < 1 or pick > min(10, len(results)):
                print("无效选择")
                return False
        except (ValueError, KeyboardInterrupt, EOFError):
            print()
            print("  非交互模式，自动选择第 1 首")
            pick = 1

    song = results[pick - 1]
    title = song.get("title") or song.get("name") or "unknown"
    author = song.get("author") or song.get("artist") or "unknown"
    sid = song.get("id")

    print("\n选中: {} - {} (id: {})".format(title, author, sid))

    safe_name = sanitize_filename("{}-{}".format(title, author))
    changed = False

    # ── 下载音频 ──────────────────────────────────────
    ext = ".m4a"
    audio_path = os.path.join(out_dir, safe_name + ext)

    if os.path.exists(audio_path):
        print("  [跳过] 已有音频 {}".format(safe_name + ext))
    else:
        # 先从搜索结果看看有没有 url，没有再通过 song API 拿
        detail_url = song.get("url")
        if not detail_url:
            detail = _get_song_detail(sid, server)
            if detail:
                detail_url = detail.get("url")

        if detail_url:
            print("  下载音频: {}".format(safe_name + ext))
            if download_file(detail_url, audio_path, "音频"):
                print("  [音频] {}".format(safe_name + ext))
                changed = True
        else:
            print("  [无音频] 该歌曲可能受版权保护")

    # ── 下载封面 ──────────────────────────────────────
    cover_path = os.path.join(out_dir, safe_name + ".jpg")
    if os.path.exists(cover_path):
        print("  [跳过] 已有封面 {}".format(safe_name + ".jpg"))
    else:
        pic_url = None
        if song.get("pic"):
            pic_url = song["pic"]
        else:
            detail = _get_song_detail(sid, server)
            if detail and detail.get("pic"):
                pic_url = detail["pic"]

        if pic_url:
            img = fetch_cover_bytes(pic_url)
            if img:
                with open(cover_path, "wb") as f:
                    f.write(img)
                print("  [封面] {}".format(safe_name + ".jpg"))
                changed = True

    # ── 下载歌词 ──────────────────────────────────────
    lrc_path = os.path.join(out_dir, safe_name + ".lrc")
    if os.path.exists(lrc_path):
        print("  [跳过] 已有歌词 {}".format(safe_name + ".lrc"))
    else:
        lrc = None
        if song.get("lrc"):
            try:
                with urllib.request.urlopen(song["lrc"], timeout=15) as resp:
                    lrc = resp.read().decode("utf-8")
            except Exception:
                pass
        if not lrc:
            lyric_id = song.get("lyric_id") or sid
            if lyric_id:
                lrc = fetch_lrc(lyric_id, server)
        if lrc:
            with open(lrc_path, "w", encoding="utf-8") as f:
                f.write(lrc)
            print("  [歌词] {} ({} 字符)".format(safe_name + ".lrc", len(lrc)))
            changed = True
        else:
            print("  [无歌词]")

    # ── 生成 md ───────────────────────────────────────
    if audio_base and md_dir is not None:
        os.makedirs(md_dir, exist_ok=True)
        audio_base = audio_base.rstrip("/") + "/"
        audio_url = audio_base + safe_name + ext
        lrc_url = audio_base + safe_name + ".lrc"
        cover_url = audio_base + safe_name + ".jpg"
        md_file = sanitize_filename(title) + ".md"
        md_path = os.path.join(md_dir, md_file)
        if os.path.exists(md_path):
            print("  [跳过] 已有 md: {}".format(md_file))
        else:
            write_markdown(md_path, title, author, audio_url, lrc_url, cover_url)
            print("  [MD] {}".format(md_file))
            changed = True

    return changed


def _get_song_detail(song_id, server="netease"):
    """获取歌曲详情"""
    url = "{}?server={}&type=song&id={}".format(
        API_BASE, server, urllib.request.quote(str(song_id)))
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data[0] if isinstance(data, list) and data else data
    except Exception:
        return None


# ── main ──────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)

    target = sys.argv[1]
    server = "netease"
    audio_base = AUDIO_BASE
    md_dir = BLOG_CONTENT_DIR
    make_md = False
    out_dir = None

    for a in sys.argv[2:]:
        if a.startswith("--server="):
            server = a.split("=", 1)[1]
        elif a.startswith("--audio-base="):
            audio_base = a.split("=", 1)[1]
        elif a == "--md":
            make_md = True
        elif a.startswith("--md-dir="):
            md_dir = os.path.abspath(a.split("=", 1)[1])
            make_md = True
        elif a == "--no-md":
            make_md = False
            md_dir = None
        elif a.startswith("--out="):
            out_dir = os.path.abspath(a.split("=", 1)[1])

    if not make_md:
        md_dir = None

    # ── 判断模式 ──────────────────────────────────────
    # target 是文件或目录 → 本地文件模式
    # target 不是路径 → 搜索下载模式，第二个参数是歌手名

    exts = {".m4a", ".aac", ".mp4", ".m4b", ".m4p", ".mp3", ".flac"}

    if os.path.isdir(target):
        # 目录模式
        files = []
        for root, _, filenames in os.walk(target):
            for f in filenames:
                if os.path.splitext(f)[1].lower() in exts:
                    files.append(os.path.abspath(os.path.join(root, f)))
        if not files:
            print("未找到音频文件")
            sys.exit(0)
        print("找到 {} 个文件\n".format(len(files)))
        ok = 0
        for f in files:
            if process_file(f, server, audio_base, md_dir):
                ok += 1
        print("\n完成: 处理了 {}/{}".format(ok, len(files)))

    elif os.path.isfile(target) and os.path.splitext(target)[1].lower() in exts:
        # 单文件模式
        print("找到 1 个文件\n")
        ok = 1 if process_file(target, server, audio_base, md_dir) else 0
        print("\n完成: 处理了 {}/1".format(ok))

    else:
        # 搜索下载模式
        # sys.argv[1] = 歌名, sys.argv[2] = 歌手（可选，不以 -- 开头）
        name = target
        artist = ""
        for a in sys.argv[2:]:
            if not a.startswith("--"):
                artist = a
                break
        process_search(name, artist, server, audio_base, md_dir, out_dir)
        print("\n完成")


if __name__ == "__main__":
    main()
