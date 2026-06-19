# Dhruv's Salon - Backend Setup Guide

## 📋 Prerequisites
- Python 3.8+ installed on your computer
- A Gmail account (for sending email notifications)

## 🚀 Setup Instructions

### Step 1: Install Python Dependencies
Open Terminal/Command Prompt in the `/Users/tejishtha/Desktop/html` folder and run:

```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (Optional but Recommended)

1. **Set up Gmail App Password:**
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification" if not already enabled
   - Go to "App passwords" section
   - Create a new app password for "Mail" and "Windows"
   - Copy the generated 16-character password

2. **Update email settings in `app.py`:**
   - Open `app.py` file
   - Find these lines around line 15-16:
     ```python
     SENDER_EMAIL = 'your-email@gmail.com'  # Change this to your email
     SENDER_PASSWORD = 'your-app-password'  # Change this to your app password
     ```
   - Replace with your Gmail and app password
   - Save the file

### Step 3: Start the Backend Server

In Terminal/Command Prompt, run:
```bash
python app.py
```

You should see:
```
🚀 Starting Flask server...
📊 Admin Dashboard: http://localhost:5000/admin
📝 API endpoint: http://localhost:5000/api/appointments
```

### Step 4: Test Your Setup

1. **Backend is running:** Visit http://localhost:5000/admin in your browser
   - You should see the Admin Dashboard with appointment statistics

2. **Frontend is working:** Open your salon website (main.html)
   - Fill in and submit an appointment form
   - You should receive confirmation emails (if email is configured)

## 📊 Admin Dashboard Features

- **View all appointments** in real-time
- **Update appointment status**: Pending → Confirmed → Completed → Cancelled
- **Track statistics**: Total appointments, pending count, revenue
- **Auto-refresh**: Updates every 30 seconds

## 🔗 API Endpoints

### POST /api/appointments
**Submit a new appointment**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "date": "2026-06-25",
  "time": "14:00",
  "services": "Haircut, Beard Trim",
  "total": 400
}
```

### GET /api/appointments
**Get all appointments**
Returns list of all appointments stored in the database.

### PUT /api/appointments/<id>
**Update appointment status**
```json
{
  "status": "confirmed"
}
```

## 📁 File Structure
```
/Users/tejishtha/Desktop/html/
├── app.py                 # Backend Flask application
├── requirements.txt       # Python dependencies
├── appointments.db        # SQLite database (auto-created)
├── main.html             # Frontend website
├── script.js             # Updated frontend script
├── style.css             # Styling
├── logo.png              # Your salon logo
```

## ⚠️ Troubleshooting

**Error: "ModuleNotFoundError: No module named 'flask'"**
- Run: `pip install -r requirements.txt`

**Error: "Address already in use"**
- Another app is using port 5000
- Change port in app.py: `app.run(debug=True, port=5001)`

**Email not sending**
- Verify Gmail app password is correct
- Check SENDER_EMAIL is correct
- Gmail app password should be 16 characters (no spaces)

**Frontend can't connect to backend**
- Make sure Flask server is running on port 5000
- Check browser console for CORS errors
- Try opening admin dashboard: http://localhost:5000/admin

## 🛑 To Stop the Server
Press `Ctrl+C` in the terminal where Flask is running.

## 💡 Next Steps (Optional)

- Set up automatic email reminders for appointments
- Add payment integration
- Deploy to cloud (Heroku, PythonAnywhere, etc.)
- Add WhatsApp notifications
- Create mobile app

---

**Need help?** Make sure both the Flask backend and your HTML frontend are accessible when testing!
