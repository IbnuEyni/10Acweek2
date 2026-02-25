# DeepSeek V3 Setup Guide

## Why DeepSeek?

- **Cheap**: $0.14/1M input tokens, $0.28/1M output tokens (70x cheaper than GPT-4)
- **Powerful**: Matches GPT-4 performance on reasoning tasks
- **No Rate Limits**: Unlike Groq's 100K tokens/day limit
- **Fast**: Similar speed to Groq

## Setup Steps

### 1. Get API Key

1. Visit: https://platform.deepseek.com/
2. Sign up (free $5 credits)
3. Go to: https://platform.deepseek.com/api_keys
4. Create new API key
5. Copy the key (starts with `sk-`)

### 2. Configure Environment

Edit `.env` file:

```bash
# Set DeepSeek as provider
LLM_PROVIDER=deepseek

# Add your API key
DEEPSEEK_API_KEY=sk-your-key-here

# Use DeepSeek Chat model
DEFAULT_LLM_MODEL=deepseek-chat
```

### 3. Test It

```bash
cd automaton-auditor
python3 src/main.py \
  --repo-url https://github.com/IbnuEyni/10Acweek2 \
  --pdf-path reports/interim_report.pdf \
  --output audit/test_deepseek.md
```

## Cost Comparison

### Groq (Free Tier)
- **Cost**: $0
- **Limit**: 100K tokens/day
- **Issue**: Hit limit after 3-4 audits

### DeepSeek
- **Cost**: ~$0.02 per audit
- **Limit**: None (pay-as-you-go)
- **Benefit**: Unlimited audits

### Example Audit Cost
- Input: ~50K tokens (evidence + prompts)
- Output: ~10K tokens (opinions)
- **Total**: $0.014 per audit

**100 audits = $1.40** 🎉

## Switching Between Providers

Just change `LLM_PROVIDER` in `.env`:

```bash
# Use Groq (free but limited)
LLM_PROVIDER=groq

# Use DeepSeek (cheap and unlimited)
LLM_PROVIDER=deepseek

# Use OpenAI (expensive but reliable)
LLM_PROVIDER=openai
```

No code changes needed!

## Troubleshooting

### Error: "DEEPSEEK_API_KEY not set"
- Make sure `.env` file has `DEEPSEEK_API_KEY=sk-...`
- Run `source .env` or restart terminal

### Error: "Invalid API key"
- Check key is correct (starts with `sk-`)
- Verify key is active at https://platform.deepseek.com/api_keys

### Slow responses
- DeepSeek V3 is large (671B parameters)
- First request may be slower (cold start)
- Subsequent requests are fast

## Model Options

### deepseek-chat (Recommended)
- Best for general tasks
- Fast and accurate
- $0.14/$0.28 per 1M tokens

### deepseek-reasoner
- Best for complex reasoning
- Slower but more thorough
- $0.55/$2.19 per 1M tokens

Change in `.env`:
```bash
DEFAULT_LLM_MODEL=deepseek-chat
# or
DEFAULT_LLM_MODEL=deepseek-reasoner
```

---

**Ready to use!** DeepSeek will now handle all judge evaluations without rate limits. 🚀
