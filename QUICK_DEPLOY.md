# Quick Deploy to Streamlit Cloud - 5 Minutes

## Step 1: Go to Streamlit Cloud
Visit: https://share.streamlit.io

## Step 2: Sign In
- Click "Sign in with GitHub"
- Authorize Streamlit to access your repositories

## Step 3: Deploy New App
1. Click **"New app"** button
2. Fill in:
   - **Repository**: `srujanj18/Resume-Screening-Agent`
   - **Branch**: `master`
   - **Main file path**: `app.py`

3. Click **"Deploy!"**

## Step 4: Add Secrets (IMPORTANT!)
Wait for deployment to complete, then:

1. Click the **three dots (⋮)** in top right
2. Select **"Settings"**
3. Go to **"Secrets"** tab
4. Add your secrets one by one:

```
GEMINI_API_KEY=your_gemini_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

5. Click **"Save"** and wait for auto-redeployment

## Step 5: Done! 🎉
Your live app will be available at:
```
https://talentflow-[username].streamlit.app
```

Share this link!

---

## Common Issues & Fixes

### "ModuleNotFoundError"
- **Cause**: Missing dependency
- **Fix**: All dependencies are in `requirements.txt` ✅

### "SUPABASE_KEY not found"
- **Cause**: Secrets not set in dashboard
- **Fix**: Follow Step 4 above carefully

### "Whisper model download timeout"
- **Cause**: Model is large (~3GB)
- **Fix**: This is normal, takes 5-10 minutes first time

### App keeps crashing
- **Check**: Streamlit Cloud logs in dashboard
- **Common cause**: Missing API keys

---

## Getting Your API Keys

### 1. Google Generative AI (Gemini)
1. Go to https://ai.google.dev
2. Create new API key
3. Copy and paste as `GEMINI_API_KEY`

### 2. Supabase Keys
1. Go to your Supabase project
2. Settings → API → Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon** key → `SUPABASE_KEY`
   - **service_role** key → `SUPABASE_SERVICE_ROLE_KEY`

---

## After Deployment

### Test the App
1. Go to your live link
2. Upload a resume PDF
3. Enter a job description
4. Start the interview
5. Try both text and voice modes
6. Generate final report

### Share with Others
- Send the live link to anyone
- No installation required
- Works on desktop and mobile (except voice on some devices)

### Updates
Every time you:
1. Push to GitHub (`git push`)
2. App auto-redeploys (1-2 minutes)
3. No manual redeploy needed!

---

## Advanced Settings (Optional)

### Custom Domain
- Premium feature in Streamlit Cloud
- Maps your domain to the app

### Scaling
- Streamlit Cloud handles scaling automatically
- No configuration needed

### Monitoring
- Check logs and metrics in dashboard
- Set up notifications

---

## Support
- **Issues**: Check DEPLOYMENT_GUIDE.md for detailed troubleshooting
- **Community**: https://discuss.streamlit.io
- **Status**: https://status.streamlit.io

---

**Your TalentFlow AI is now live on the internet! 🚀**
