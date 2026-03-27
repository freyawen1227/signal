#!/usr/bin/env python3
"""
Feishu Sync Script for YouTube Learning Assistant
Automatically syncs output.md to Feishu document and sends notification.
Supports OAuth authorization so documents are created by the user (not bot).
"""

import json
import re
import argparse
import urllib.request
import urllib.error
import time
import webbrowser
import http.server
import threading
from pathlib import Path
from urllib.parse import urlencode, parse_qs, urlparse

# Configuration
SKILL_DIR = Path.home() / ".claude" / "skills" / "youtube-learning-assistant"
CONFIG_FILE = SKILL_DIR / "config" / "feishu.json"
TOKEN_FILE = SKILL_DIR / "config" / "user_token.json"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
REDIRECT_URI = "http://localhost:8765/callback"
LOCAL_PORT = 8765


def load_config():
    """Load Feishu configuration from config file."""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def api_request(method, endpoint, token=None, data=None, retries=3):
    """Make API request to Feishu with retry logic."""
    url = f"{FEISHU_API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method
        )

        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                print(f"  ⏳ Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            error_body = e.read().decode()
            print(f"API Error: {e.code} - {error_body}")
            raise


def load_user_token():
    """Load saved user token if exists."""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def save_user_token(token_data):
    """Save user token to file."""
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler to receive OAuth callback."""
    auth_code = None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/callback":
            query = parse_qs(parsed.query)
            if "code" in query:
                OAuthCallbackHandler.auth_code = query["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("✅ 授权成功！可以关闭此页面。".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authorization failed")

    def log_message(self, format, *args):
        pass  # Suppress logging


def get_auth_url(config):
    """Generate OAuth authorization URL."""
    params = {
        "app_id": config["app_id"],
        "redirect_uri": REDIRECT_URI,
        "state": "youtube_learning",
        "scope": "docx:document docx:document:create"
    }
    return f"https://open.feishu.cn/open-apis/authen/v1/authorize?{urlencode(params)}"


def wait_for_auth_code():
    """Start local server and wait for OAuth callback."""
    OAuthCallbackHandler.auth_code = None  # Reset
    server = http.server.HTTPServer(("localhost", LOCAL_PORT), OAuthCallbackHandler)
    server.timeout = 120  # 2 minutes timeout

    print("  🌐 等待浏览器授权...")
    while OAuthCallbackHandler.auth_code is None:
        server.handle_request()

    server.server_close()
    return OAuthCallbackHandler.auth_code


def exchange_code_for_token(config, code):
    """Exchange authorization code for user access token."""
    # First get app_access_token
    app_token_result = api_request("POST", "/auth/v3/app_access_token/internal", data={
        "app_id": config["app_id"],
        "app_secret": config["app_secret"]
    })
    app_token = app_token_result["app_access_token"]

    # Exchange code for user token
    result = api_request("POST", "/authen/v1/oidc/access_token", app_token, {
        "grant_type": "authorization_code",
        "code": code
    })

    if result.get("code") != 0:
        raise Exception(f"Token exchange failed: {result}")

    return {
        "access_token": result["data"]["access_token"],
        "refresh_token": result["data"]["refresh_token"],
        "expires_at": time.time() + result["data"]["expires_in"] - 60  # 60s buffer
    }


def refresh_user_token(config, refresh_token):
    """Refresh user access token."""
    # Get app_access_token
    app_token_result = api_request("POST", "/auth/v3/app_access_token/internal", data={
        "app_id": config["app_id"],
        "app_secret": config["app_secret"]
    })
    app_token = app_token_result["app_access_token"]

    # Refresh token
    result = api_request("POST", "/authen/v1/oidc/refresh_access_token", app_token, {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })

    if result.get("code") != 0:
        return None  # Token expired, need re-auth

    return {
        "access_token": result["data"]["access_token"],
        "refresh_token": result["data"]["refresh_token"],
        "expires_at": time.time() + result["data"]["expires_in"] - 60
    }


def get_user_access_token(config):
    """Get user access token, with OAuth flow if needed."""
    token_data = load_user_token()

    # Check if token exists and not expired
    if token_data:
        if time.time() < token_data.get("expires_at", 0):
            return token_data["access_token"]

        # Try to refresh
        print("  🔄 刷新用户令牌...")
        new_token = refresh_user_token(config, token_data["refresh_token"])
        if new_token:
            save_user_token(new_token)
            return new_token["access_token"]

    # Need OAuth authorization
    print("  📱 首次使用需要授权，正在打开浏览器...")
    auth_url = get_auth_url(config)
    webbrowser.open(auth_url)

    # Wait for callback
    code = wait_for_auth_code()
    print("  ✅ 收到授权码")

    # Exchange for token
    token_data = exchange_code_for_token(config, code)
    save_user_token(token_data)
    print("  💾 令牌已保存，下次无需重新授权")

    return token_data["access_token"]


def get_tenant_access_token(config):
    """Get tenant access token (for sending messages)."""
    result = api_request("POST", "/auth/v3/tenant_access_token/internal", data={
        "app_id": config["app_id"],
        "app_secret": config["app_secret"]
    })
    return result["tenant_access_token"]


def get_access_token(config):
    """Get tenant access token from Feishu."""
    result = api_request("POST", "/auth/v3/tenant_access_token/internal", data={
        "app_id": config["app_id"],
        "app_secret": config["app_secret"]
    })
    return result["tenant_access_token"]


def create_document(token, title):
    """Create a new Feishu document."""
    result = api_request("POST", "/docx/v1/documents", token, {
        "title": title,
        "folder_token": ""
    })
    return result["data"]["document"]["document_id"]


def parse_markdown_to_blocks(markdown_content):
    """Parse markdown content and convert to Feishu block format."""
    blocks = []
    lines = markdown_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip horizontal rules
        if line == "---":
            i += 1
            continue

        # Heading 1: # Title
        if line.startswith("# ") and not line.startswith("## "):
            # Skip the title (already in document title)
            i += 1
            continue

        # Heading 1: ## Section
        if line.startswith("## "):
            blocks.append({
                "block_type": 3,
                "heading1": {
                    "elements": [{"text_run": {"content": line[3:], "text_element_style": {}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Heading 2: ### Subsection
        if line.startswith("### "):
            blocks.append({
                "block_type": 4,
                "heading2": {
                    "elements": [{"text_run": {"content": line[4:], "text_element_style": {}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Bold metadata: **来源**: xxx
        if line.startswith("**") and "**:" in line:
            blocks.append({
                "block_type": 2,
                "text": {
                    "elements": [{"text_run": {"content": line.replace("**", ""), "text_element_style": {}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Quote: > text
        if line.startswith("> "):
            blocks.append({
                "block_type": 2,
                "text": {
                    "elements": [{"text_run": {"content": line[2:], "text_element_style": {"italic": True}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Bullet list: - item or • item
        if line.startswith("- ") or line.startswith("• "):
            prefix = "• " if not line.startswith("• ") else ""
            content = line[2:] if line.startswith("- ") else line
            blocks.append({
                "block_type": 2,
                "text": {
                    "elements": [{"text_run": {"content": prefix + content.lstrip("• "), "text_element_style": {}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Numbered list: 1. item
        if re.match(r"^\d+\.\s", line):
            blocks.append({
                "block_type": 2,
                "text": {
                    "elements": [{"text_run": {"content": line, "text_element_style": {}}}],
                    "style": {}
                }
            })
            i += 1
            continue

        # Table: | col | col |
        if line.startswith("|"):
            # Collect all table lines
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_line = lines[i].strip()
                # Skip separator line
                if not re.match(r"^\|[-:\s|]+\|$", table_line):
                    table_lines.append(table_line)
                i += 1

            # Convert table to text
            for tl in table_lines:
                cells = [c.strip() for c in tl.split("|")[1:-1]]
                blocks.append({
                    "block_type": 2,
                    "text": {
                        "elements": [{"text_run": {"content": " | ".join(cells), "text_element_style": {}}}],
                        "style": {}
                    }
                })
            continue

        # Regular text paragraph
        # Collect consecutive text lines
        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line or next_line.startswith("#") or next_line.startswith("-") or \
               next_line.startswith(">") or next_line.startswith("|") or next_line == "---" or \
               re.match(r"^\d+\.\s", next_line):
                break
            para_lines.append(next_line)
            i += 1

        content = " ".join(para_lines)
        # Check for bold patterns and handle them
        content = re.sub(r"\*\*([^*]+)\*\*", r"\1", content)

        blocks.append({
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": content, "text_element_style": {}}}],
                "style": {}
            }
        })

    return blocks


def write_blocks_to_document(token, doc_id, blocks, batch_size=10):
    """Write blocks to Feishu document in batches with rate limiting."""
    index = 0
    total_batches = (len(blocks) + batch_size - 1) // batch_size
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        batch_num = i // batch_size + 1
        print(f"  📤 Writing batch {batch_num}/{total_batches}...")
        api_request("POST", f"/docx/v1/documents/{doc_id}/blocks/{doc_id}/children", token, {
            "children": batch,
            "index": index
        })
        index += len(batch)
        # Add delay between batches to avoid rate limiting
        if i + batch_size < len(blocks):
            time.sleep(0.5)
    return index


def send_notification(token, config, title, description, source, duration, doc_id, video_url):
    """Send Feishu notification to user with rich card format."""
    doc_url = f"https://uasbnk1zod4.feishu.cn/docx/{doc_id}"

    card_content = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "📚 视频学习笔记已生成"},
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{title}**\n\n{description}"
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {"tag": "lark_md", "content": f"**来源**\n{source}"}
                    },
                    {
                        "is_short": True,
                        "text": {"tag": "lark_md", "content": f"**时长**\n{duration}"}
                    }
                ]
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "📖 查看完整笔记"},
                        "type": "primary",
                        "url": doc_url
                    },
                    {
                        "tag": "button",
                        "text": {"tag": "plain_text", "content": "🎬 观看原视频"},
                        "type": "default",
                        "url": video_url
                    }
                ]
            }
        ]
    }

    api_request("POST", "/im/v1/messages?receive_id_type=open_id", token, {
        "receive_id": config["open_id"],
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    })


def extract_metadata_from_markdown(markdown_content):
    """Extract metadata from markdown for notification card."""
    lines = markdown_content.split("\n")

    # Default values
    source = "YouTube"
    duration = ""
    description = ""
    key_points = []

    for i, line in enumerate(lines):
        line = line.strip()

        # Extract source: **平台**: YouTube
        if line.startswith("**平台**:"):
            source = line.replace("**平台**:", "").strip()

        # Extract duration: **时长**: 1:20:35
        if line.startswith("**时长**:"):
            duration = line.replace("**时长**:", "").strip()

        # Extract description from 总结 section
        if line == "## 总结":
            # Next non-empty line is the description
            for j in range(i + 1, min(i + 10, len(lines))):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith("#"):
                    description = next_line  # Keep full content
                    break

    # Extract key points from Insight or key sections
    # Look for bullet points after certain headings
    in_insight = False
    for line in lines:
        line = line.strip()
        if "## Insight" in line or "核心要点" in line:
            in_insight = True
            continue
        if in_insight and line.startswith("## "):
            break
        if in_insight and (line.startswith("- ") or line.startswith("• ")):
            point = line.lstrip("-•").strip()
            # Shorten if too long
            if len(point) > 50:
                point = point[:47] + "..."
            key_points.append(point)
            if len(key_points) >= 3:
                break

    # If no key points found, create generic ones
    if not key_points:
        key_points = ["视频核心内容已整理", "专业术语已解释", "业务启发已提炼"]

    return {
        "source": source,
        "duration": duration,
        "description": description,
        "key_points": key_points
    }


def main():
    parser = argparse.ArgumentParser(description="Sync markdown to Feishu document")
    parser.add_argument("--markdown", required=True, help="Path to output.md file")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--url", required=True, help="Original video URL")
    args = parser.parse_args()

    # Load config
    config = load_config()

    # Read markdown content
    with open(args.markdown, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    print(f"📄 Read markdown file: {args.markdown}")

    # Get user access token (for creating document as user)
    print("🔐 获取用户授权...")
    user_token = get_user_access_token(config)
    print("🔑 Got user access token")

    # Create document with user token (user is the owner)
    doc_title = f"{args.title} - 学习笔记"
    doc_id = create_document(user_token, doc_title)
    print(f"📝 Created Feishu document: {doc_id}")

    # Parse and write blocks
    blocks = parse_markdown_to_blocks(markdown_content)
    print(f"🔄 Parsed {len(blocks)} blocks from markdown")

    write_blocks_to_document(user_token, doc_id, blocks)
    print(f"✅ Wrote all blocks to document")

    # Extract metadata for notification
    metadata = extract_metadata_from_markdown(markdown_content)

    # Get tenant token for sending message (bot sends notification)
    bot_token = get_tenant_access_token(config)

    # Send notification
    send_notification(
        bot_token, config, args.title,
        metadata["description"],
        metadata["source"],
        metadata["duration"],
        doc_id, args.url
    )
    print("📬 Sent notification to Feishu")

    doc_url = f"https://uasbnk1zod4.feishu.cn/docx/{doc_id}"
    print(f"\n🎉 Done! Document URL: {doc_url}")


if __name__ == "__main__":
    main()
