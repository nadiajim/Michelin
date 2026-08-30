"""
Push local git repository to GitHub using Dulwich
Supports personal access token (PAT) or username/password.
"""
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dulwich.repo import Repo
from dulwich import porcelain
from dulwich.client import get_transport_and_path

def push_repo(token=None):
    repo_path = os.path.abspath(os.path.dirname(__file__))
    repo = Repo(repo_path)
    
    remote_url = "https://github.com/nadiajim/Michelin.git"
    if token:
        remote_url = f"https://{token}@github.com/nadiajim/Michelin.git"
    
    print(f"Pushing to {remote_url.split('@')[-1]} ...")
    try:
        porcelain.push(repo, remote_url, refspecs=[b"refs/heads/master:refs/heads/main", b"refs/heads/main:refs/heads/main"])
        print("[SUCCESS] Successfully pushed all files to https://github.com/nadiajim/Michelin!")
    except Exception as e:
        print(f"[ERROR] Push failed: {e}")
        print("\nTo push, GitHub requires authentication (Personal Access Token).")
        print("Run: python push_to_github.py <YOUR_GITHUB_TOKEN>")

if __name__ == "__main__":
    github_token = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_TOKEN")
    push_repo(github_token)
