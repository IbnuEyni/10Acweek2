"""
Git tools for safe repository operations.
Implements sandboxed cloning, history analysis, and edge case handling.
"""
import subprocess
import tempfile
import re
from pathlib import Path
from typing import List, Dict, Optional
from src.utils.config import Config
from src.utils.sandbox import isolated_directory, run_sandboxed_command, SandboxViolation


def validate_repo_url(repo_url: str) -> bool:
    """
    Validate GitHub repository URL format.
    
    Args:
        repo_url: Repository URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Match github.com URLs (https or git protocol)
    patterns = [
        r'^https://github\.com/[\w-]+/[\w.-]+(\.git)?$',
        r'^git@github\.com:[\w-]+/[\w.-]+(\.git)?$'
    ]
    return any(re.match(pattern, repo_url) for pattern in patterns)


def safe_clone_repo(repo_url: str) -> Path:
    """
    Clone repository to isolated temporary directory with sandboxing.
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Path to cloned repository
        
    Raises:
        ValueError: If URL invalid, clone fails, or repo empty
    """
    # Validate URL format
    if not validate_repo_url(repo_url):
        raise ValueError(f"Invalid GitHub URL format: {repo_url}")
    
    temp_dir = tempfile.mkdtemp(prefix="audit_repo_")
    
    try:
        # Use sandboxed command execution with resource limits
        result = run_sandboxed_command(
            ["git", "clone", "--depth", "50", repo_url, temp_dir],
            timeout=Config.GIT_CLONE_TIMEOUT
        )
        
        repo_path = Path(temp_dir)
        
        # Check if repo is empty
        py_files = list(repo_path.rglob("*.py"))
        if not py_files:
            raise ValueError("Repository contains no Python files")
        
        return repo_path
        
    except SandboxViolation as e:
        raise ValueError(f"Sandbox violation: {str(e)}")
    except subprocess.TimeoutExpired:
        raise ValueError(f"Clone timeout after {Config.GIT_CLONE_TIMEOUT}s")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.lower()
        if "not found" in error_msg or "repository not found" in error_msg:
            raise ValueError(f"Repository not found: {repo_url}")
        elif "authentication" in error_msg or "permission denied" in error_msg:
            raise ValueError(f"Authentication failed (private repo?): {repo_url}")
        else:
            raise ValueError(f"Clone failed: {e.stderr}")


def extract_git_history(repo_path: Path) -> List[Dict[str, str]]:
    """
    Extract commit history with messages and timestamps.
    Handles empty repos gracefully.
    
    Args:
        repo_path: Path to cloned repository
        
    Returns:
        List of commits with hash, message, timestamp (empty list if no commits)
    """
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--reverse", "--format=%H|%s|%ai"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():
            return []  # Empty repo
        
        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|", 2)
                if len(parts) == 3:
                    hash_val, message, timestamp = parts
                    commits.append({
                        "hash": hash_val,
                        "message": message,
                        "timestamp": timestamp
                    })
        
        return commits
    except subprocess.CalledProcessError:
        return []  # Graceful degradation


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
