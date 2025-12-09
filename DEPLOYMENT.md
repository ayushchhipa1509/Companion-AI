# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deployment Steps

### 1. Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Memory & Personality Engine"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

   ⚠️ **Important**: Make sure your repository is **PUBLIC** (Streamlit Cloud free tier requires public repos)

### 2. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**:
   - Click **"New app"** button
   - Select **"Use existing repo"**
   - Choose your repository from the dropdown
   - Set **Main file path**: `app.py`
   - Click **"Deploy"**

3. **Configure Secrets** (CRITICAL):
   - After deployment starts, go to **"Settings"** (⚙️ icon)
   - Click **"Secrets"** tab
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "sk-your-actual-key-here"
     ```
   - Click **"Save"**

4. **Wait for Deployment**:
   - Streamlit will install dependencies from `requirements.txt`
   - Build process takes 1-2 minutes
   - Your app will be live at: `https://your-app-name.streamlit.app`

### 3. Verify Deployment

1. **Check the App**:
   - Open your Streamlit Cloud URL
   - You should see "✅ API key loaded from Secrets" in the sidebar
   - Test memory extraction with sample chats
   - Test before/after personality comparison

2. **Common Issues**:
   - **Build fails**: Check `requirements.txt` is correct
   - **API key error**: Verify secrets are configured correctly
   - **Import errors**: Ensure all files are in the repo (check `.gitignore`)

### 4. Update Your README

Before submitting, update these links in `README.md`:
- Replace `[Your repo link]` with your actual GitHub URL
- Replace `[Your Streamlit Cloud link]` with your Streamlit Cloud URL

## File Checklist

Before deploying, ensure you have:

- ✅ `app.py` (main Streamlit app)
- ✅ `modules/memory.py` (memory extraction)
- ✅ `modules/personality.py` (personality engine)
- ✅ `modules/__init__.py` (package init)
- ✅ `data/sample_chats.json` (sample data)
- ✅ `requirements.txt` (dependencies)
- ✅ `README.md` (documentation)
- ✅ `.gitignore` (excludes secrets/local files)

## Testing Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Test:
1. Load sample chats
2. Extract memory
3. Compare before/after responses
4. Try different personality styles

## Troubleshooting

### Build Fails
- Check `requirements.txt` has correct package names
- Ensure Python version compatibility (Streamlit Cloud uses Python 3.9+)

### API Key Not Working
- Verify secrets format (must be TOML)
- Check key starts with `sk-`
- Ensure no extra spaces or quotes

### Import Errors
- Verify all files are committed to Git
- Check `modules/__init__.py` exists
- Ensure file paths are correct (case-sensitive on Linux)

### App Crashes
- Check Streamlit Cloud logs (Settings → Logs)
- Verify API key is valid
- Test locally first to catch errors

## Success Criteria

Your deployment is successful when:
- ✅ App loads without errors
- ✅ API key is recognized from secrets
- ✅ Memory extraction works
- ✅ Before/after comparison shows different responses
- ✅ All personality styles work
- ✅ Sample data loads correctly

---

**Need Help?** Check Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud

