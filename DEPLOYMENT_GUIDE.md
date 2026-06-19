# 🚀 Free Website Hosting & Notifications Setup Guide

This guide will help you host your salon website and dashboard for **completely free** with real-time notifications visible worldwide.

## 📋 What You'll Get

✅ **Website hosted globally** (Vercel)
✅ **Backend API & Dashboard** (Railway)
✅ **Email notifications** (Gmail)
✅ **Real-time appointment updates** from anywhere in the world
✅ **Custom domain support** (optional)

---

## 🌐 Frontend Hosting - Vercel (Free)

### Step 1: Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up"
3. Choose "Continue with GitHub" (or email)
4. Connect your GitHub account

### Step 2: Deploy Your Website

**Option A: Using Git (Recommended)**

```bash
# 1. Initialize Git in your project folder
cd /Users/tejishtha/Desktop/html
git init

# 2. Create a GitHub repository at github.com/new
# 3. Add and push your files
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/salon-website.git
git push -u origin main

# 4. On Vercel dashboard, click "Add New > Project"
# 5. Select your GitHub repository
# 6. Vercel will auto-detect and deploy!
```

**Option B: Direct Upload**

1. Go to [vercel.com/new](https://vercel.com/new)
2. Choose "Other" or upload folder directly
3. Deploy!

✅ Your website will be live at: `https://your-project-name.vercel.app`

---

## 🔧 Backend Hosting - Railway (Free)

### Step 1: Prepare Backend
```bash
# Make sure you have updated requirements.txt with:
# - gunicorn
# - python-dotenv

# Create environment configuration
echo "FLASK_ENV=production
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password" > .env
```

### Step 2: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Start Project"
3. Sign up with GitHub

### Step 3: Deploy Backend
1. Click "Create New Project"
2. Select "GitHub Repo" (or upload via CLI)
3. Select your repository
4. Railway auto-detects Python/Flask
5. Set environment variables:
   - `FLASK_ENV`: production
   - `SENDER_EMAIL`: your gmail
   - `SENDER_PASSWORD`: your app password
6. Deploy!

✅ Your backend will be live at: `https://your-project.railway.app`

---

## 📧 Email Setup (Gmail)

### Required: Create Gmail App Password

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable "2-Step Verification" (if not enabled)
3. Go to "App passwords"
4. Select "Mail" and "Windows"
5. Copy the 16-character password
6. Add to your `.env` file:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## 📊 Access Your Dashboard

Once deployed, access your dashboard at:

```
https://your-backend.railway.app/admin
```

Or use the HTML dashboard we created:
```
https://your-project.vercel.app/admin-dashboard.html
```

### Dashboard Features:
- 📈 Real-time appointment statistics
- 📅 View all bookings
- 🔄 Auto-refresh every 5 seconds
- 📍 See bookings from worldwide
- ⏰ Latest appointments first

---

## 🔗 Connect Frontend to Backend

Update your frontend code to use the production backend URL:

**In `/main.html` (line ~135):**
```javascript
// Change from:
fetch('http://localhost:5001/api/appointments', {

// To:
fetch('https://your-backend.railway.app/api/appointments', {
```

**In `/admin-dashboard.html` (line ~250):**
```javascript
// Change from:
const API_URL = 'http://localhost:5001'

// To:
const API_URL = 'https://your-backend.railway.app'
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`:
   ```
   .env
   *.db
   __pycache__/
   .DS_Store
   ```

2. **Keep credentials secure**:
   - Don't share your Gmail app password
   - Use environment variables in production
   - Enable 2FA on all accounts

3. **Database backup**:
   - Railway provides PostgreSQL as free upgrade
   - Consider using it instead of SQLite for production

---

## ✅ Testing Your Setup

### Local Testing:
```bash
# 1. Start Flask server
python app.py

# 2. In another terminal, start frontend
# Open main.html in browser

# 3. Fill a test appointment form
# 4. Check admin dashboard at http://localhost:5001/admin
# 5. Verify email sent
```

### Production Testing:
1. Visit your Vercel website
2. Fill an appointment form
3. Check admin dashboard at `https://your-backend.railway.app/admin`
4. Verify email sent to your Gmail
5. Dashboard should update in real-time

---

## 💰 Cost Analysis

| Service | Free Tier | Price |
|---------|-----------|-------|
| **Vercel** | Unlimited deployments | Always Free |
| **Railway** | $5/month free credits | Pay-as-you-go |
| **Gmail** | App passwords | Always Free |
| **Custom Domain** | Optional | $10-15/year |

**Total Cost: $0-5/month!**

---

## 🆘 Troubleshooting

### Dashboard shows "Offline"
- Check backend URL in code
- Make sure Railway deployment is running
- Check network tab in browser DevTools

### Emails not sending
- Verify Gmail app password is correct
- Check SENDER_EMAIL is set
- Allow "Less secure apps" in Gmail settings

### Vercel build fails
- Check all imports are available
- Ensure required files are committed
- View deployment logs on Vercel dashboard

### Railway deployment fails
- Check Procfile exists
- Verify requirements.txt is formatted correctly
- Check for Python syntax errors

---

## 🎯 Next Steps

1. ✅ Create accounts on Vercel and Railway
2. ✅ Deploy frontend to Vercel
3. ✅ Deploy backend to Railway
4. ✅ Update URLs in code
5. ✅ Test appointment booking
6. ✅ Test admin dashboard
7. ✅ Share your website with customers!

---

## 📱 Your URLs After Deployment

- **Website**: https://salon-site.vercel.app
- **Dashboard**: https://salon-api.railway.app/admin
- **API**: https://salon-api.railway.app/api/appointments

Share the website link with customers - they can book from anywhere in the world! 🌍

---

**Questions?** Check the README files or review your provider's documentation:
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Flask Guide](https://flask.palletsprojects.com)

Happy hosting! 🚀
