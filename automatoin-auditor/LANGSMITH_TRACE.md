# LangSmith Trace - Quick Access

## View Full Execution Trace

**LangSmith Dashboard**: https://smith.langchain.com/

**Project Name**: `automaton-auditor`

**Steps**:
1. Visit https://smith.langchain.com/
2. Sign in with your account
3. Click "Projects" → "automaton-auditor"
4. View all audit execution traces

## What You'll See

- **Timeline View**: Complete execution flow from start to finish
- **LLM Calls**: All 4 LLM interactions (1 Gemini + 3 DeepSeek)
- **Parallel Execution**: Visual representation of fan-out/fan-in
- **Performance**: Token counts, latency, execution time
- **Debugging**: Inputs/outputs for each node

## Generate Public URL (Optional)

1. Open any trace in dashboard
2. Click "Share" button (top right)
3. Enable "Public" sharing
4. Copy URL (format: `https://smith.langchain.com/public/<trace-id>/r`)

## Configuration

Tracing is enabled via `.env`:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=automaton-auditor
LANGSMITH_API_KEY=<your_langsmith_api_key>
```

## Recent Execution

**Date**: February 27, 2026 23:15:45  
**Repository**: https://github.com/IbnuEyni/10Acweek2  
**Evidence**: 7 categories collected  
**Opinions**: 12 judicial opinions  
**Duration**: ~45 seconds  
**Score**: 3.50/5.0

---

**Full Documentation**: See `TRACE_DOCUMENTATION.md` for detailed information
