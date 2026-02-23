"""
deploy_vercel.py — Deploy the portfolio to Vercel via REST API
Run: python deploy_vercel.py
Requires: pip install requests
Get token: https://vercel.com/account/tokens
"""

import requests
import json
import base64
import os
import sys

# ── CONFIG ────────────────────────────────────────────────
VERCEL_TOKEN = "PASTE_YOUR_VERCEL_TOKEN_HERE"   # <-- get from vercel.com/account/tokens
PROJECT_NAME = "niraja-portfolio"
# ─────────────────────────────────────────────────────────

BASE = "d:/hackathon/portfolio"

FILES = [
    ("app.py",                   "app.py"),
    ("requirements.txt",         "requirements.txt"),
    ("vercel.json",              "vercel.json"),
    ("templates/index.html",     "templates/index.html"),
    ("static/css/style.css",     "static/css/style.css"),
    ("static/resume.pdf",        "static/resume.pdf"),
]

def encode_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def deploy():
    if VERCEL_TOKEN == "PASTE_YOUR_VERCEL_TOKEN_HERE":
        print("❌ Please set your VERCEL_TOKEN in this script first!")
        print("   Get it from: https://vercel.com/account/tokens")
        sys.exit(1)

    print("📦 Encoding files...")
    files = []
    for local, remote in FILES:
        full = os.path.join(BASE.replace("/", "\\"), local.replace("/", "\\"))
        if not os.path.exists(full):
            print(f"  ⚠ Skipping missing: {full}")
            continue
        files.append({
            "file": remote,
            "data": encode_file(full),
            "encoding": "base64"
        })
        print(f"  ✓ {remote}")

    payload = {
        "name": PROJECT_NAME,
        "files": files,
        "projectSettings": {
            "framework": None,
            "buildCommand": None,
            "outputDirectory": None,
            "installCommand": "pip install flask groq gunicorn",
        },
        "routes": [{"src": "/(.*)", "dest": "app.py"}]
    }

    print("\n🚀 Deploying to Vercel...")
    r = requests.post(
        "https://api.vercel.com/v13/deployments",
        headers={
            "Authorization": f"Bearer {VERCEL_TOKEN}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )

    if r.status_code in (200, 201):
        data = r.json()
        url = data.get("url") or data.get("alias", [""])[0]
        print(f"\n✅ Deployed! Your live URL is:")
        print(f"   https://{url}")
    else:
        print(f"\n❌ Deployment failed ({r.status_code}):")
        print(r.text[:500])

if __name__ == "__main__":
    deploy()
