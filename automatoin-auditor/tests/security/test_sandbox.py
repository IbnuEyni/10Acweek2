"""
Security test suite for sandboxing implementation.
Verifies resource limits, path traversal protection, and shell injection prevention.
"""
import pytest
from pathlib import Path
from src.utils.sandbox import (
    ResourceLimits,
    SandboxViolation,
    run_sandboxed_command,
    validate_file_access
)


class TestResourceLimits:
    """Test resource limit configuration."""
    
    def test_memory_limit_configured(self):
        """Verify memory limit is set to reasonable value."""
        assert ResourceLimits.MAX_MEMORY_MB == 1024
        assert ResourceLimits.MAX_MEMORY_MB >= 512
    
    def test_cpu_limit_configured(self):
        """Verify CPU time limit prevents runaway processes."""
        assert ResourceLimits.MAX_CPU_TIME_SEC == 60
        assert ResourceLimits.MAX_CPU_TIME_SEC >= 30
    
    def test_process_limit_configured(self):
        """Verify process limit allows git forking."""
        assert ResourceLimits.MAX_PROCESSES == 100
        assert ResourceLimits.MAX_PROCESSES >= 50
    
    def test_file_size_limit_configured(self):
        """Verify file size limit prevents large file attacks."""
        assert ResourceLimits.MAX_FILE_SIZE_MB == 10
        assert ResourceLimits.MAX_FILE_SIZE_MB <= 50


class TestPathTraversalProtection:
    """Test path traversal attack prevention."""
    
    def test_blocks_etc_passwd(self):
        """Verify /etc/passwd access is blocked."""
        with pytest.raises(SandboxViolation, match="Path traversal detected"):
            validate_file_access(Path("/etc/passwd"))
    
    def test_allows_tmp_files(self):
        """Verify /tmp files are allowed (for cloned repos)."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test")
            temp_path = Path(f.name)
        
        try:
            validate_file_access(temp_path, max_size_mb=10)
        finally:
            temp_path.unlink()


class TestShellInjectionPrevention:
    """Test shell injection attack prevention."""
    
    def test_blocks_semicolon_injection(self):
        """Verify semicolon command chaining is blocked."""
        with pytest.raises(SandboxViolation, match="Shell metacharacters not allowed"):
            run_sandboxed_command(["echo", "test; rm -rf /"], apply_limits=False)
    
    def test_blocks_pipe_injection(self):
        """Verify pipe command chaining is blocked."""
        with pytest.raises(SandboxViolation, match="Shell metacharacters not allowed"):
            run_sandboxed_command(["echo", "test | cat /etc/passwd"], apply_limits=False)
    
    def test_allows_safe_commands(self):
        """Verify safe commands execute successfully."""
        result = run_sandboxed_command(["echo", "hello world"], apply_limits=False)
        assert result.stdout.strip() == "hello world"


class TestTimeoutEnforcement:
    """Test timeout enforcement prevents hanging processes."""
    
    def test_timeout_kills_long_running_command(self):
        """Verify commands exceeding timeout are killed."""
        with pytest.raises(SandboxViolation, match="Command timeout after 2s"):
            run_sandboxed_command(["sleep", "100"], timeout=2, apply_limits=False)


class TestFileSizeValidation:
    """Test file size validation prevents large file attacks."""
    
    def test_blocks_oversized_files(self):
        """Verify files exceeding size limit are rejected."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("x" * (11 * 1024 * 1024))
            temp_path = Path(f.name)
        
        try:
            with pytest.raises(SandboxViolation, match="File too large"):
                validate_file_access(temp_path, max_size_mb=10)
        finally:
            temp_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
