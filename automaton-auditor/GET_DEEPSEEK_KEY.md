# Get DeepSeek API Key - Step by Step

## Steps to Get Your Key:

1. **Open Browser**: Go to https://platform.deepseek.com/

2. **Sign Up**: 
   - Click "Sign Up" or "Get Started"
   - Use email or GitHub login
   - Verify your email

3. **Get Free Credits**:
   - New accounts get $5 free credits
   - Enough for ~250 audits

4. **Create API Key**:
   - Go to: https://platform.deepseek.com/api_keys
   - Click "Create API Key"
   - Copy the key (starts with `sk-`)

5. **Add to .env**:
   - Replace `sk-your-key-here` with your actual key
   - Save the file

## Alternative: Use Groq (Wait for Reset)

If you don't want to sign up for DeepSeek right now, you can:

1. **Wait for Groq Reset** (~24 hours from last use)
2. **Change .env**:
   ```
   LLM_PROVIDER=groq
   ```
3. **Run audit** when rate limit resets

## Or Test with Current Setup

If you already have a DeepSeek key, just:
1. Replace `sk-your-key-here` in .env with your real key
2. Save
3. Run the test command below

---

Once you have the key, run:
```bash
cd automaton-auditor
PYTHONPATH=$PWD:$PYTHONPATH python3 src/main.py \
  --repo-url /home/shuaib/Desktop/python/10Acweek2 \
  --pdf-path reports/interim_report.pdf \
  --output audit/report_deepseek_test.md
```
