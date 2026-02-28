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


def safe_clone_repo(repo_url: str, max_retries: int = 2) -> Path:
    """
    Clone repository to isolated temporary directory with sandboxing.
    Includes retry logic for network issues.
    
    Args:
        repo_url: GitHub repository URL
        max_retries: Number of retry attempts for network failures
        
    Returns:
        Path to cloned repository
        
    Raises:
        ValueError: If URL invalid, clone fails, or repo empty
    """
    # Validate URL format
    if not validate_repo_url(repo_url):
        raise ValueError(f"Invalid GitHub URL format: {repo_url}")
    
    last_error = None
    
    for attempt in range(max_retries + 1):
        temp_dir = tempfile.mkdtemp(prefix="audit_repo_")
        
        try:
            # Use sandboxed command execution without resource limits for git
            # (git needs to fork multiple processes)
            result = run_sandboxed_command(
                ["git", "clone", "--depth", "50", repo_url, temp_dir],
                timeout=120,  # Increased timeout for Streamlit
                apply_limits=False  # Git needs process forking
            )
            
            repo_path = Path(temp_dir)
            
            # Check if repo is empty
            py_files = list(repo_path.rglob("*.py"))
            if not py_files:
                raise ValueError("Repository contains no Python files")
            
            return repo_path
            
        except (SandboxViolation, subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            last_error = e
            # Clean up failed attempt
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
            
            # Don't retry on authentication or not found errors
            if isinstance(e, subprocess.CalledProcessError):
                error_msg = str(e).lower()
                if "not found" in error_msg or "authentication" in error_msg:
                    break
            
            # Retry on network/timeout errors
            if attempt < max_retries:
                continue
    
    # All retries failed
    if isinstance(last_error, SandboxViolation):
        raise ValueError(f"Sandbox violation: {str(last_error)}")
    elif isinstance(last_error, subprocess.TimeoutExpired):
        raise ValueError(f"Clone timeout after 120s (tried {max_retries + 1} times)")
    elif isinstance(last_error, subprocess.CalledProcessError):
        error_msg = getattr(last_error, 'stderr', str(last_error)).lower()
        if "not found" in error_msg or "repository not found" in error_msg:
            raise ValueError(f"Repository not found: {repo_url}")
        elif "authentication" in error_msg or "permission denied" in error_msg:
            raise ValueError(f"Authentication failed (private repo?): {repo_url}")
        else:
            raise ValueError(f"Clone failed after {max_retries + 1} attempts: {last_error}")
    else:
        raise ValueError(f"Clone failed: {last_error}")


def extract_git_history(repo_path: Path) -> List[Dict[str, str]]:
    """
    Extract commit history with messages and timestamps.
    Handles empty repos gracefully.
    
    Security Note:
    --------------
    The format string '%H|%s|%ai' contains pipe characters (|) which are
    NOT shell metacharacters in this context. This is a git-specific format
    string passed as an argument to git log, not executed by the shell.
    
    Git format placeholders:
    - %H: Full commit hash
    - %s: Commit subject (message)
    - %ai: Author date (ISO 8601 format)
    - |: Delimiter (literal character, not shell pipe)
    
    The command is executed via subprocess.run with shell=False, ensuring
    the format string is treated as a literal argument, not shell code.
    
    Args:
        repo_path: Path to cloned repository
        
    Returns:
        List of commits with hash, message, timestamp (empty list if no commits)
    """
    try:
        result = run_sandboxed_command(
            ["git", "log", "--oneline", "--reverse", "--format=%H|%s|%ai"],
            cwd=str(repo_path),
            timeout=30,
            apply_limits=False
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
        result = run_sandboxed_command(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=str(repo_path),
            timeout=10,
            apply_limits=False
        )
        return int(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError):
        return 0
