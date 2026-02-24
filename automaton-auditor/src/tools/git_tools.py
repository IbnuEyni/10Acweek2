"""
Git tools for safe repository operations.
Implements sandboxed cloning and history analysis.
"""
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from src.utils.config import Config


def safe_clone_repo(repo_url: str) -> Path:
    """
    Clone repository to isolated temporary directory.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Path to cloned repository
        
    Raises:
        ValueError: If clone fails
    """
    temp_dir = tempfile.mkdtemp(prefix="audit_repo_")
    
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "50", repo_url, temp_dir],
            capture_output=True,
            text=True,
            timeout=Config.GIT_CLONE_TIMEOUT,
            check=True
        )
        return Path(temp_dir)
    except subprocess.TimeoutExpired:
        raise ValueError(f"Clone timeout after {Config.GIT_CLONE_TIMEOUT}s")
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Clone failed: {e.stderr}")


def extract_git_history(repo_path: Path) -> List[Dict[str, str]]:
    """
    Extract commit history with messages and timestamps.
    
    Args:
        repo_path: Path to cloned repository
        
    Returns:
        List of commits with hash, message, timestamp
    """
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--reverse", "--format=%H|%s|%ai"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                hash_val, message, timestamp = line.split("|", 2)
                commits.append({
                    "hash": hash_val,
                    "message": message,
                    "timestamp": timestamp
                })
        
        return commits
    except subprocess.CalledProcessError:
        return []


def count_commits(repo_path: Path) -> int:
    """Count total commits in repository."""
    try:
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return 0
