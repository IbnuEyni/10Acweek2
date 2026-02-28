# Streamlit Demo Quick Start

## Running the Streamlit App

```bash
cd /home/shuaib/Desktop/python/10Acweek2/automatoin-auditor
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Using the App

1. **Enter Repository URL**: `https://github.com/IbnuEyni/10Acweek2`
2. **Upload PDF** (optional): Upload `reports/final_report.pdf` or leave blank
3. **Click "🚀 Run Audit"**
4. **Wait for completion** (~30-60 seconds)
5. **View results** in 3 tabs:
   - 📄 Full Report
   - 📊 Evidence (10 categories)
   - ⚖️ Opinions (30 judicial opinions from 3 judges)

## Expected Results

- **Evidence Collected**: 10 categories
- **Judicial Opinions**: 30 (10 criteria × 3 judges)
- **Overall Score**: 4.10-4.20/5.0
- **Report Size**: ~47,000 characters

## Report Saving

Reports are automatically saved to:
```
audit/streamlit_runs/audit_report_YYYYMMDD_HHMMSS.md
```

## Video Recording Tips

1. **Clear browser cache** before recording
2. **Set zoom to 100%**
3. **Close unnecessary tabs**
4. **Use full screen mode** (F11)
5. **Narrate as you go**:
   - "Entering repository URL..."
   - "Running audit with parallel execution..."
   - "Detectives collecting evidence..."
   - "Judges deliberating with distinct personas..."
   - "Chief Justice synthesizing final verdict..."

## Troubleshooting

If the app doesn't start:
```bash
# Check if port 8501 is in use
lsof -i :8501

# Kill existing Streamlit process
pkill -f streamlit

# Try again
streamlit run app.py
```

## Testing Without Browser

Run the test script to verify everything works:
```bash
python3 test_streamlit_flow.py
```

This simulates the exact workflow Streamlit uses.
