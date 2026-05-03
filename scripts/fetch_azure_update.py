#!/usr/bin/env python3
"""
Fetch the latest Azure Update video from the Microsoft Azure YouTube playlist
and create a Jekyll/Chirpy blog post from it.

Required environment variable:
    YOUTUBE_API_KEY  — A Google Cloud API key with YouTube Data API v3 enabled.

Usage:
    python scripts/fetch_azure_update.py
"""

import os
import re
import sys

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PLAYLIST_ID = "PLlVtbbG169nGL0hj1CeL2Zjmr73SmXIpc"
POSTS_DIR = "_posts"
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


# ---------------------------------------------------------------------------
# YouTube helpers
# ---------------------------------------------------------------------------

def get_latest_video(api_key: str, playlist_id: str) -> dict:
    """Return metadata for the most recent video in *playlist_id*."""
    url = f"{YOUTUBE_API_BASE}/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 1,
        "key": api_key,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    items = data.get("items", [])
    if not items:
        print("No videos found in the playlist.")
        sys.exit(1)

    snippet = items[0]["snippet"]
    video_id = snippet["resourceId"]["videoId"]
    thumbnails = snippet.get("thumbnails", {})
    thumbnail_url = (
        thumbnails.get("maxres", {}).get("url")
        or thumbnails.get("high", {}).get("url")
        or thumbnails.get("default", {}).get("url")
        or ""
    )

    return {
        "video_id": video_id,
        "title": snippet["title"],
        "description": snippet.get("description", "").strip(),
        "published_at": snippet["publishedAt"],
        "thumbnail_url": thumbnail_url,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
    }


# ---------------------------------------------------------------------------
# Post helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Return a URL-safe slug derived from *text*."""
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def post_exists(video_id: str, posts_dir: str) -> bool:
    """Return True if a post containing *video_id* already exists."""
    if not os.path.isdir(posts_dir):
        return False
    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as fh:
            if video_id in fh.read():
                return True
    return False


def _format_description(description: str) -> str:
    """Return a markdown-safe, reasonably sized version of the description."""
    if not description:
        return "_No description provided._"
    lines = description.splitlines()
    if len(lines) > 30:
        lines = lines[:30]
        lines.append("")
        lines.append("_[Description truncated — view the full video on YouTube for details.]_")
    return "\n".join(lines)


def create_blog_post(video: dict, posts_dir: str) -> str:
    """Write a Jekyll/Chirpy markdown post and return its file path."""
    # Derive date and filename from the video's publish timestamp
    # publishedAt is in RFC 3339 / ISO 8601 format: "2025-12-23T17:00:00Z"
    post_date = video["published_at"][:10]  # "YYYY-MM-DD"
    slug = slugify(video["title"])[:60].rstrip("-")
    filename = f"{post_date}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)

    # Escape double quotes inside the title for YAML
    title_yaml = video["title"].replace("\\", "\\\\").replace('"', '\\"')

    description_md = _format_description(video["description"])
    video_id = video["video_id"]
    video_url = video["video_url"]

    # Build optional image frontmatter block
    image_block = ""
    if video["thumbnail_url"]:
        image_block = (
            f"image:\n"
            f"  path: {video['thumbnail_url']}\n"
            f"  alt: \"{title_yaml}\"\n"
        )

    # Chirpy YouTube embed tag (Liquid, written as a raw string in the file)
    youtube_embed = "{{% include embed/youtube.html id='{vid}' %}}".format(vid=video_id)

    content = (
        "---\n"
        f'title: "{title_yaml}"\n'
        f"date: {post_date}\n"
        "categories:\n"
        "  - azure\n"
        "  - azure-updates\n"
        "tags:\n"
        "  - azure-updates\n"
        "  - microsoft-azure\n"
        f"{image_block}"
        "---\n"
        "\n"
        "## Azure Update: Weekly Summary\n"
        "\n"
        "The latest **Azure Update** video has been published on the "
        "[Microsoft Azure YouTube channel](https://www.youtube.com/playlist"
        f"?list={PLAYLIST_ID}).\n"
        "\n"
        f"{youtube_embed}\n"
        "\n"
        "## Overview\n"
        "\n"
        f"{description_md}\n"
        "\n"
        "---\n"
        f"*Source: [Microsoft Azure — Azure Updates Playlist]({video_url})*\n"
    )

    os.makedirs(posts_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(content)

    return filepath


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    api_key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable is not set.")
        sys.exit(1)

    print(f"Fetching latest video from playlist: {PLAYLIST_ID}")
    video = get_latest_video(api_key, PLAYLIST_ID)
    print(f"Latest video: {video['title']} (ID: {video['video_id']})")

    if post_exists(video["video_id"], POSTS_DIR):
        print(
            f"A post for video '{video['video_id']}' already exists — nothing to do."
        )
        sys.exit(0)

    filepath = create_blog_post(video, POSTS_DIR)
    print(f"Created blog post: {filepath}")


if __name__ == "__main__":
    main()
