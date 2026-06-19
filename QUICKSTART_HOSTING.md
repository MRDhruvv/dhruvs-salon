# ⚡ Quick Start - Free Hosting & Notifications

Get your salon website live worldwide in 5 minutes!

## 🎯 Step 1: Setup Email (2 minutes)

1. Go to [Gmail Security Settings](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Generate "App Password"
4. Copy the 16-character password

## 🎯 Step 2: Create `.env` File (1 minute)

In your project folder, create a file named `.env`:

```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
FLASK_ENV=production
```

**⚠️ IMPORTANT: Add to `.gitignore` - never commit this file!**

## 🎯 Step 3: Deploy Frontend (1 minute)

### Using Vercel (Easiest)

```bash
# 1. Sign up at vercel.com with GitHub
# 2. Import your repository
# 3. Deploy!
```

✅ Your site will be live at: **https://your-project.vercel.app**

## 🎯 Step 4: Deploy Backend (1 minute)

### Using Railway

1. Sign up at [railway.app](https://railway.app)
2. Create new project → GitHub repo
3. Add environment variables:
   - `SENDER_EMAIL`: your-email@gmail.com
   - `SENDER_PASSWORD`: your-app-password
4. Deploy!

✅ Your API will be live at: **https://your-project.railway.app**

## 🎯 Step 5: Update URLs

Replace these in your code:

**main.html (line ~135):**
```javascript
fetch('https://your-project.railway.app/api/appointments', {
```

**admin-dashboard.html (line ~250):**
```javascript
const API_URL = 'https://your-project.railway.app'
```

## 🌐 You're Done! 

### Your URLs:
- 🌍 **Website**: https://your-project.vercel.app
- 📊 **Dashboard**: https://your-project.railway.app/admin
- 📱 **Share website** with customers to get bookings!

---

## 📊 What You Get:

✅ Website hosted globally
✅ Real-time appointment notifications
✅ Email confirmations  
✅ Admin dashboard visible worldwide
✅ 100% FREE (no credit card needed)

---

## 🆘 Need Help?

**Site not loading?**
- Check Vercel deployment logs

**Bookings not showing?**
- Verify backend URL is correct
- Check Railway is running

**Emails not sending?**
- Check `.env` file has correct password
- Verify app password was created in Gmail

---

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.
