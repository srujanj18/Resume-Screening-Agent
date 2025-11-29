# Streamlit Cloud Deployment Guide - TalentFlow AI

## Prerequisites
- GitHub account with your repository pushed
- Streamlit account (free at https://streamlit.io)
- Supabase project with credentials
- Google Generative AI API key

## Step 1: Prepare Repository

Your repository is already pushed to GitHub at:
```
https://github.com/srujanj18/Resume-Screening-Agent
```

Ensure all required files are committed:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `utils/` (all utility files)
- ✅ `data/` (if needed)

## Step 2: Set Up Streamlit Cloud Deployment

### Option A: Deploy via Streamlit Cloud Dashboard (Recommended)

1. **Go to Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account

2. **Create New App**:
   - Click "New app"
   - Select repository: `srujanj18/Resume-Screening-Agent`
   - Select branch: `master`
   - Set file path: `app.py`

3. **Configure Secrets**:
   - Click "Advanced settings"
   - Paste your secrets in the format:
     ```
     GEMINI_API_KEY = "your_key"
     SUPABASE_URL = "your_url"
     SUPABASE_KEY = "your_key"
     SUPABASE_SERVICE_ROLE_KEY = "your_key"
     ```
   - Click "Deploy"

4. **Live App URL**:
   - Your app will be available at:
   ```
   https://talentflow-[your-username].streamlit.app
   ```

### Option B: Deploy via CLI

1. **Install Streamlit CLI**:
   ```bash
   pip install streamlit
   ```

2. **Login to Streamlit**:
   ```bash
   streamlit login
   ```
   - Copy the authentication token from your browser
   - Paste it in the terminal

3. **Deploy**:
   ```bash
   streamlit run app.py --deploy
   ```

## Step 3: Add Streamlit Configuration

Create `.streamlit/config.toml` in your project:

```toml
[client]
showErrorDetails = true
maxMessageSize = 200

[logger]
level = "info"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Step 4: Optimize for Streamlit Cloud

### Memory & Performance Tips:
1. **Caching**: Whisper model is already cached with `@st.cache_resource`
2. **Session State**: Already implemented for multi-page experience
3. **File Uploads**: PDF processing is efficient

### Potential Issues & Solutions:

#### Issue: Whisper Model Too Large (>2GB)
**Solution**: Use "base" model instead of "turbo" in `app.py`:
```python
whisper_model = load_whisper("base")  # Smaller, faster
```

#### Issue: Timeout on Long Operations
**Solution**: Already handled with spinners and progress indicators

#### Issue: Storage Space
- Streamlit Cloud provides 1GB of storage
- Temporary audio files are cleaned up automatically
- Consider implementing cloud storage for PDFs

## Step 5: Monitor Deployment

After deployment:
1. Check app logs in Streamlit Cloud dashboard
2. Monitor resource usage
3. Set up email alerts for crashes

## Step 6: Update & Redeploy

**To update your live app**:
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add -A
   git commit -m "Update: description"
   git push origin master
   ```
3. Streamlit Cloud automatically redeploys on push (within 1-2 minutes)

## Environment Variables for Streamlit Cloud

In Streamlit Cloud dashboard, set secrets as:
```
GEMINI_API_KEY="sk-..."
SUPABASE_URL="https://xxxxx.supabase.co"
SUPABASE_KEY="eyJhbGc..."
SUPABASE_SERVICE_ROLE_KEY="eyJhbGc..."
```

## Troubleshooting

### App Won't Deploy
- Check GitHub repo is public
- Verify `requirements.txt` includes all dependencies
- Check `.streamlit/secrets.toml` is in `.gitignore`

### Database Connection Fails
- Verify SUPABASE_SERVICE_ROLE_KEY is set in Streamlit Cloud secrets
- Check Supabase project is active
- Ensure `candidates` table exists

### Whisper Model Downloads Fail
- Network timeout is common with large models
- Use smaller model: `whisper.load_model("base")`
- Or pre-download model locally and commit

### Out of Memory
- Reduce Whisper model size
- Implement garbage collection
- Use smaller PDF processing batches

## Performance Optimization

### Current Implementation
- ✅ Whisper model caching
- ✅ Session state for efficiency
- ✅ Temp file cleanup
- ✅ Proper error handling

### Future Improvements
- Implement response caching for API calls
- Add rate limiting
- Compress audio before Whisper processing
- Use async operations for DB calls

## Support & Monitoring

- **Streamlit Cloud Status**: https://status.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **Logs**: Available in Streamlit Cloud dashboard

---

## Quick Deployment Checklist

- [ ] Push to GitHub
- [ ] Create Streamlit Cloud account
- [ ] Connect GitHub to Streamlit
- [ ] Deploy app
- [ ] Set secrets in dashboard
- [ ] Test all features
- [ ] Share live link

**Your live demo link will be**:
```
https://talentflow-[your-username].streamlit.app
```

Share this with recruiters and interviewers!
