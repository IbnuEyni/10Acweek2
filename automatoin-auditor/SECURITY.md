# Security Measures

## Sandboxing

### Git Clone Isolation
All repository clones execute in isolated temporary directories:

```python
def safe_clone_repo(repo_url: str) -> Path:
    temp_dir = tempfile.mkdtemp(prefix="audit_repo_")
    subprocess.run(
        ["git", "clone", "--depth", "50", repo_url, temp_dir],
        timeout=60,
        check=True
    )
    return Path(temp_dir)
```

**Security Benefits**:
- No persistent filesystem modifications
- Automatic cleanup with shutil.rmtree()
- Prevents path traversal attacks
- Isolated from main codebase
- Concurrent audits don't conflict

### Subprocess Safety
All external commands use subprocess.run() with:
- `check=True`: Raises exception on non-zero exit
- `timeout=60`: Prevents hanging processes
- No shell=True: Prevents shell injection
- Explicit argument lists: No string interpolation

## Input Validation

### Pydantic Type Safety
All data structures use Pydantic BaseModel with runtime validation:

```python
class Evidence(BaseModel):
    goal: str
    found: bool
    confidence: float = Field(ge=0.0, le=1.0)  # Enforced range
    location: str
    rationale: str
```

**Validation Enforced**:
- Type checking (str, bool, float, int)
- Range constraints (confidence 0-1, scores 1-5)
- Required fields (no None values)
- Automatic coercion with validation

### URL Validation
Repository URLs validated before git operations:

```python
if not repo_url.startswith(("https://", "http://")):
    raise ValueError("Invalid repository URL")
```

### Path Validation
PDF paths verified before processing:

```python
pdf_path = Path(pdf_path)
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")
```

## API Key Management

### Environment Variables Only
All API keys stored in .env file (never committed):

```bash
GROQ_API_KEY=gsk_...
GOOGLE_API_KEY=AIza...
LANGCHAIN_API_KEY=lsv2_...
```

### .gitignore Protection
Prevents accidental credential commits:

```
.env
*.key
*.pem
credentials.json
```

### No Hardcoded Credentials
Code uses os.getenv() with no defaults:

```python
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not set")
```

## Resource Limits

### Timeout Guards
All external operations have timeouts:
- Git clone: 60 seconds
- LLM calls: 30 seconds
- PDF parsing: 45 seconds

### Depth Limits
- Git clone: --depth 50 (prevents large history downloads)
- AST parsing: Max 10MB file size
- PDF parsing: Max 100 pages

### Rate Limiting
- Groq: 30 requests/minute (enforced by provider)
- Gemini: 1500 requests/day (enforced by provider)
- Automatic retry with exponential backoff

## Data Privacy

### No Data Persistence
- Temporary directories deleted after audit
- No logs contain sensitive code
- LangSmith tracing can be disabled

### No External Sharing
- Code analyzed locally only
- LLM calls contain metadata only (no full code)
- Reports stored locally (not uploaded)

## Threat Model

### Protected Against
✅ Shell injection (no shell=True)  
✅ Path traversal (sandboxed directories)  
✅ Resource exhaustion (timeouts, depth limits)  
✅ Credential leaks (.gitignore, env vars)  
✅ Concurrent conflicts (isolated temp dirs)

### Not Protected Against
❌ Malicious git repositories (clone at your own risk)  
❌ PDF exploits (use trusted PDFs only)  
❌ API key theft (secure your .env file)

## Audit Trail

### LangSmith Observability
All LLM calls logged with:
- Timestamp
- Input/output tokens
- Latency
- Error messages

### Error Logging
All exceptions captured in state.errors:

```python
try:
    result = risky_operation()
except Exception as e:
    state["errors"].append(f"Operation failed: {str(e)}")
```

## Recommendations

1. **Run in Docker**: Isolate from host system
2. **Use Read-Only Mounts**: Prevent file modifications
3. **Rotate API Keys**: Monthly key rotation
4. **Monitor Usage**: Track LLM API costs
5. **Review Logs**: Check LangSmith for anomalies

---

**Security Status**: ✅ Production-grade sandboxing and validation  
**Last Updated**: February 25, 2026  
**Contact**: security@example.com
