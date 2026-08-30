"""
Git initialization and commit manager using Dulwich
"""
import os
import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dulwich.repo import Repo
from dulwich import porcelain

repo_path = os.path.abspath(os.path.dirname(__file__))

# Initialize repo if not already initialized
if not os.path.exists(os.path.join(repo_path, ".git")):
    repo = Repo.init(repo_path)
    print(f"[OK] Initialized new Git repository at: {repo_path}")
else:
    repo = Repo(repo_path)
    print(f"[OK] Existing Git repository found at: {repo_path}")

# Add all tracked files
porcelain.add(repo_path)
print("[OK] Staged all project files")

# Commit
try:
    commit_id = porcelain.commit(
        repo_path,
        message="Initial commit: Michelin Veterinary Clinical Co-Pilot with Gemini & Google Cloud (All Things Agentic Hackathon)",
        author="Nadia Jiménez <nadia@example.com>",
        committer="Nadia Jiménez <nadia@example.com>"
    )
    print(f"[OK] Created initial commit: {commit_id.decode('ascii')}")
except Exception as e:
    print(f"[NOTE] Commit status: {e}")

# Set remote origin
config = repo.get_config()
remote_url = b"https://github.com/nadiajim/Michelin.git"
config.set((b"remote", b"origin"), b"url", remote_url)
config.set((b"remote", b"origin"), b"fetch", b"+refs/heads/*:refs/remotes/origin/*")
config.write_to_path()
print(f"[OK] Configured remote origin: {remote_url.decode('ascii')}")
