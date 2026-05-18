# Grok API Setup Guide

## Step 1: Get Your Grok API Key

1. Visit **https://console.x.ai/**
2. Sign up or log in with your xAI account
3. Navigate to **API Keys** section
4. Click **Create New Key**
5. Copy your API key

## Step 2: Configure Environment Variable

### Option A: Using .env file (Recommended)

1. Open `.env` file in the project root directory
2. Update the line:
   ```
   GROK_API_KEY=your_actual_grok_api_key_here
   ```
3. Save the file

### Option B: Using System Environment Variable

**Windows (Command Prompt):**
```batch
set GROK_API_KEY=your_actual_grok_api_key_here
set LLM_PROVIDER=grok
```

**Windows (PowerShell):**
```powershell
$env:GROK_API_KEY="your_actual_grok_api_key_here"
$env:LLM_PROVIDER="grok"
```

## Step 3: Run the App

```bash
cd "c:\asad\Courses AI\karachi AI\GEN AI\Week 6\Homework"
streamlit run app.py
```

## Step 4: Test with Your Data

1. Open http://localhost:8501
2. Go to **📊 Data Input** tab
3. Upload any of these files:
   - `data/Refund_Claims_Data_Fixed.csv`
   - `data/customer_complaints.xlsx`
4. Click **🚀 Start Processing** in the Processing tab
5. Monitor for any errors in the Streamlit console

## Switching Back to OpenAI (if needed)

To use OpenAI instead, set:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

## Troubleshooting

**Error: "GROK_API_KEY is not set"**
- Make sure your `.env` file is in the project root
- Restart Streamlit after creating/updating `.env`
- Verify the key is correct at https://console.x.ai/

**Error: API connection issues**
- Check your internet connection
- Verify Grok API is accessible at https://api.x.ai/v1
- Check API key validity at https://console.x.ai/

**Error: Rate limit exceeded**
- Check your usage at https://console.x.ai/
- Wait a moment before retrying


