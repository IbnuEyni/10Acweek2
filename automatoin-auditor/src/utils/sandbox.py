"""
Sandboxing utilities for secure code execution and analysis.
Implements resource limits, isolation, and security controls.
"""
import subprocess
import tempfile
import shutil
import resource
import signal
from pathlib import Path
from typing import Optional, Dict, Any
from contextlib import contextmanager


class SandboxViolation(Exception):
    """Raised when sandbox security policy is violated."""
    pass


class ResourceLimits:
    """Resource limits for sandboxed operations."""
    MAX_MEMORY_MB = 1024  # Increased for git operations
    MAX_CPU_TIME_SEC = 60
    MAX_FILE_SIZE_MB = 10
    MAX_PROCESSES = 100  # Git needs multiple processes


def set_resource_limits():
    """Apply resource limits to current process (Unix only)."""
    try:
        # Memory limit (soft limit only to allow some flexibility)
        memory_bytes = ResourceLimits.MAX_MEMORY_MB * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes * 2))
        
        # CPU time limit
        resource.setrlimit(resource.RLIMIT_CPU, (ResourceLimits.MAX_CPU_TIME_SEC, ResourceLimits.MAX_CPU_TIME_SEC + 30))
        
        # Process limit (generous for git)
        resource.setrlimit(resource.RLIMIT_NPROC, (ResourceLimits.MAX_PROCESSES, ResourceLimits.MAX_PROCESSES + 50))
    except (ValueError, OSError, AttributeError):
        pass  # Windows or insufficient permissions


@contextmanager
def isolated_directory():
    """
    Context manager for isolated temporary directory.
    Automatically cleans up on exit.
    """
    temp_dir = tempfile.mkdtemp(prefix="sandbox_")
    try:
        yield Path(temp_dir)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_sandboxed_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    timeout: int = 30,
    env: Optional[Dict[str, str]] = None,
    apply_limits: bool = True
) -> subprocess.CompletedProcess:
    """
    Execute command in sandboxed environment with resource limits.
    
    Args:
        cmd: Command and arguments
        cwd: Working directory
        timeout: Timeout in seconds
        env: Environment variables
        apply_limits: Whether to apply resource limits (disable for git)
        
    Returns:
        CompletedProcess result
        
    Raises:
        SandboxViolation: If security policy violated
        subprocess.TimeoutExpired: If timeout exceeded
    """
    # Validate command
    if not cmd or not isinstance(cmd, list):
        raise SandboxViolation("Invalid command format")
    
    # Prevent shell injection
    if any(c in str(cmd) for c in [';', '|', '&', '$', '`']):
        raise SandboxViolation("Shell metacharacters not allowed")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
            env=env,
            shell=False,  # Critical: no shell
            preexec_fn=set_resource_limits if apply_limits else None
        )
        return result
    except subprocess.CalledProcessError as e:
        raise SandboxViolation(f"Command failed: {e.stderr}")
    except subprocess.TimeoutExpired:
        raise SandboxViolation(f"Command timeout after {timeout}s")


def validate_file_access(file_path: Path, max_size_mb: int = 10) -> None:
    """
    Validate file is safe to access.
    
    Args:
        file_path: Path to validate
        max_size_mb: Maximum file size in MB
        
    Raises:
        SandboxViolation: If file unsafe
    """
    if not file_path.exists():
        raise SandboxViolation(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise SandboxViolation(f"Not a file: {file_path}")
    
    # Check size
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        raise SandboxViolation(f"File too large: {size_mb:.1f}MB > {max_size_mb}MB")
    
    # Check path traversal (allow /tmp for cloned repos)
    resolved = file_path.resolve()
    if not (str(resolved).startswith(str(Path.cwd())) or str(resolved).startswith('/tmp')):
        raise SandboxViolation("Path traversal detected")
