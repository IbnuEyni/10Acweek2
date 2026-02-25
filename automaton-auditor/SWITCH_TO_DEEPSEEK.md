# Quick: Switch to DeepSeek to Avoid Rate Limits

## Problem
Groq free tier: 100K tokens/day limit (hit after 3-4 audits)

## Solution
Switch to DeepSeek: $0.02/audit, no limits

## Steps

### 1. Get DeepSeek API Key (2 minutes)
```bash
# Visit: https://platform.deepseek.com/api_keys
# Sign up (free $5 credits)
# Create API key (starts with sk-)
```

### 2. Update .env File
```bash
cd automaton-auditor

# Add these lines to .env:
echo "LLM_PROVIDER=deepseek" >> .env
echo "DEEPSEEK_API_KEY=sk-your-key-here" >> .env
echo "DEFAULT_LLM_MODEL=deepseek-chat" >> .env
```

### 3. Run Audit
```bash
PYTHONPATH=/home/shuaib/Desktop/python/10Acweek2/automaton-auditor:$PYTHONPATH \
python3 src/main.py \
  --repo-url /home/shuaib/Desktop/python/10Acweek2 \
  --pdf-path /home/shuaib/Desktop/python/10Acweek2/automaton-auditor/reports/interim_report.pdf \
  --output audit/report_deepseek.md
```

## Done!

No more rate limits. Cost: ~$0.02 per audit.

---

## Alternative: Wait for Groq Reset

Groq rate limit resets every 24 hours.

Check when it resets:
```bash
# Last error said: "Please try again in 12m42s"
# Wait that long, then re-run audit
```

---

## Comparison

| Provider | Cost/Audit | Daily Limit | Speed |
|----------|-----------|-------------|-------|
| Groq     | $0        | 3-4 audits  | Fast  |
| DeepSeek | $0.02     | Unlimited   | Fast  |
| OpenAI   | $0.50     | High        | Fast  |

**Recommendation**: Use DeepSeek for unlimited audits at minimal cost.
