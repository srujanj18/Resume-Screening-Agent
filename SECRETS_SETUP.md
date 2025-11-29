# Setting Up Secrets in Streamlit Cloud - REQUIRED!

Your app is deployed but failing because API keys are missing. Follow these steps:

## Step 1: Go to Your App Settings
1. Visit: https://share.streamlit.io
2. Find your app: **resumescreeningagent-fmuugwqybpqmxvphejkyb3**
3. Click the **three dots (⋮)** in the top right
4. Select **"Settings"**

## Step 2: Add Secrets
1. Click the **"Secrets"** tab on the left
2. Copy and paste ALL of these (replace with your actual keys):

```
GEMINI_API_KEY = "your_gemini_api_key_here"
SUPABASE_URL = "your_supabase_url_here"
SUPABASE_KEY = "your_supabase_anon_key_here"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role_key_here"
```

## Step 3: Save and Reboot
1. Click **"Save"**
2. The app will automatically redeploy (wait 1-2 minutes)
3. Your app should now work! ✅

---

## Getting Your Keys

### 1. GEMINI_API_KEY
- Go to: https://ai.google.dev/
- Click **"Get API Key"**
- Create a new key for "Resume-Screening-Agent"
- Copy the key

### 2. SUPABASE Keys
- Go to your Supabase project: https://supabase.com
- Click **"Settings"** → **"API"**
- Copy:
  - **Project URL** → `SUPABASE_URL`
  - **anon public** key → `SUPABASE_KEY`
  - **service_role** secret → `SUPABASE_SERVICE_ROLE_KEY`

---

## Format in Streamlit Cloud

**IMPORTANT**: The secrets format in Streamlit Cloud is slightly different from local:

```
GEMINI_API_KEY = "sk-..."
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGc..."
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGc..."
```

**Note**: No quotes around the key names, use `=` not `:`, one secret per line.

---

## Troubleshooting

### Still getting KeyError?
- Check the spelling of the secret name (case-sensitive)
- Wait 2-3 minutes for the app to redeploy
- Try refreshing the browser (Ctrl+F5)

### App still won't load?
- Check Streamlit Cloud logs (visible in the dashboard)
- Verify all 4 secrets are added
- Make sure keys are correct (copy-paste carefully)

---

## After Adding Secrets

Once you save, Streamlit Cloud will:
1. 🔄 Redeploy your app (1-2 minutes)
2. ✅ App will load successfully
3. 🎉 All features will work!

**Go back to**: https://resumescreeningagent-fmuugwqybpqmxvphejkyb3.streamlit.app

---

**Your app is live and ready once secrets are configured!**
