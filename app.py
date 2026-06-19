from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///appointments.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Email configuration - Reads from environment variables
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'your-app-password')

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    services = db.Column(db.String(500), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'date': self.date,
            'time': self.time,
            'services': self.services,
            'total': self.total,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }

# Create database tables
with app.app_context():
    db.create_all()

def send_email(to_email, subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def send_customer_confirmation(appointment):
    """Send confirmation email to customer"""
    subject = "Appointment Confirmation - Dhruv's Unisex Salon"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #b01a26;">✓ Appointment Confirmed</h2>
                <p>Hi <strong>{appointment.name}</strong>,</p>
                <p>Your appointment at Dhruv's Unisex Salon has been confirmed!</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">Appointment Details:</h3>
                    <p><strong>Date:</strong> {appointment.date}</p>
                    <p><strong>Time:</strong> {appointment.time}</p>
                    <p><strong>Services:</strong> {appointment.services}</p>
                    <p><strong>Total:</strong> ₹{appointment.total:.2f}</p>
                </div>
                
                <p><strong>Location:</strong> 174 Buttar Road, Dharampura Mohalla, Qadian, Punjab</p>
                <p><strong>Phone:</strong> +91 6283210354</p>
                
                <p>If you need to reschedule or cancel, please call us or reply to this email.</p>
                <p>We look forward to serving you!</p>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">Dhruv's Unisex Salon & Spa</p>
            </div>
        </body>
    </html>
    """
    return send_email(appointment.email, subject, body)

def send_admin_notification(appointment):
    """Send notification email to admin"""
    subject = f"New Appointment Booking - {appointment.name}"
    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #b01a26;">📅 New Appointment Booking</h2>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
                    <p><strong>Customer Name:</strong> {appointment.name}</p>
                    <p><strong>Email:</strong> {appointment.email}</p>
                    <p><strong>Phone:</strong> {appointment.phone}</p>
                    <p><strong>Date:</strong> {appointment.date}</p>
                    <p><strong>Time:</strong> {appointment.time}</p>
                    <p><strong>Services:</strong> {appointment.services}</p>
                    <p><strong>Total Amount:</strong> ₹{appointment.total:.2f}</p>
                    <p><strong>Booking Time:</strong> {appointment.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <p>View all appointments in the <a href="http://localhost:5001/admin">Admin Dashboard</a></p>
            </div>
        </body>
    </html>
    """
    return send_email(SENDER_EMAIL, subject, body)

# ==================== STATIC FILE ROUTES ====================

@app.route('/')
def home():
    """Serve main.html at root"""
    with open('main.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/main.html')
def main():
    """Serve main.html"""
    with open('main.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/admin-dashboard.html')
def dashboard():
    """Serve admin dashboard"""
    with open('admin-dashboard.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/admin')
def admin():
    """Serve old admin dashboard"""
    with open('admin-dashboard.html', 'r', encoding='utf-8') as f:
        return f.read()

# ==================== API ROUTES ====================

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """Receive appointment booking from frontend"""
    try:
        data = request.json
        
        appointment = Appointment(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            date=data.get('date'),
            time=data.get('time'),
            services=data.get('services'),
            total=data.get('total')
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # Send emails
        send_customer_confirmation(appointment)
        send_admin_notification(appointment)
        
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully!',
            'appointment_id': appointment.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error booking appointment: {str(e)}'
        }), 400

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments"""
    try:
        appointments = Appointment.query.order_by(Appointment.created_at.desc()).all()
        return jsonify({
            'success': True,
            'appointments': [a.to_dict() for a in appointments]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update appointment status"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'message': 'Appointment not found'}), 404
        
        data = request.json
        if 'status' in data:
            appointment.status = data['status']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'appointment': appointment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Delete an appointment"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'message': 'Appointment not found'}), 404
        
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Appointment deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

# Admin Dashboard HTML
ADMIN_DASHBOARD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Dhruv's Salon</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Montserrat', Arial, sans-serif;
            margin: 0;
            background: linear-gradient(120deg, #3a0b0b, #1b0505);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #b01a26;
            margin-top: 0;
            text-align: center;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #ff9f7a, #ffd6c2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: #5a1200;
        }
        .stat-card h3 {
            margin: 0 0 10px;
            font-size: 14px;
        }
        .stat-card .number {
            font-size: 32px;
            font-weight: 800;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background-color: #b01a26;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 700;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }
        .status.pending {
            background-color: #fff3cd;
            color: #856404;
        }
        .status.confirmed {
            background-color: #d4edda;
            color: #155724;
        }
        .status.completed {
            background-color: #d1ecf1;
            color: #0c5460;
        }
        .status.cancelled {
            background-color: #f8d7da;
            color: #721c24;
        }
        button {
            background: #b01a26;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }
        button:hover {
            background: #8a1520;
        }
        .services-list {
            font-size: 12px;
            color: #666;
        }
        .no-data {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        select {
            padding: 6px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📅 Appointment Management Dashboard</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Appointments</h3>
                <div class="number" id="total">0</div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="number" id="pending-count">0</div>
            </div>
            <div class="stat-card">
                <h3>Confirmed</h3>
                <div class="number" id="confirmed-count">0</div>
            </div>
            <div class="stat-card">
                <h3>Total Revenue</h3>
                <div class="number" id="revenue">₹0</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Date & Time</th>
                    <th>Services</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody id="appointments-list">
                <tr><td colspan="8" class="no-data">Loading appointments...</td></tr>
            </tbody>
        </table>
    </div>

    <script>
        async function loadAppointments() {
            try {
                const response = await fetch('http://localhost:5001/api/appointments');
                const data = await response.json();
                
                if (data.success) {
                    displayAppointments(data.appointments);
                    updateStats(data.appointments);
                }
            } catch (error) {
                console.error('Error loading appointments:', error);
                document.getElementById('appointments-list').innerHTML = 
                    '<tr><td colspan="8" class="no-data">Error loading appointments</td></tr>';
            }
        }

        function displayAppointments(appointments) {
            const tbody = document.getElementById('appointments-list');
            
            if (appointments.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="no-data">No appointments yet</td></tr>';
                return;
            }
            
            tbody.innerHTML = appointments.map(apt => `
                <tr>
                    <td><strong>${apt.name}</strong></td>
                    <td>${apt.email}</td>
                    <td>${apt.phone}</td>
                    <td>${apt.date} ${apt.time}</td>
                    <td><div class="services-list">${apt.services}</div></td>
                    <td><strong>₹${apt.total.toFixed(2)}</strong></td>
                    <td>
                        <select onchange="updateStatus(${apt.id}, this.value)">
                            <option value="pending" ${apt.status === 'pending' ? 'selected' : ''}>
                                <span class="status pending">Pending</span>
                            </option>
                            <option value="confirmed" ${apt.status === 'confirmed' ? 'selected' : ''}>Confirmed</option>
                            <option value="completed" ${apt.status === 'completed' ? 'selected' : ''}>Completed</option>
                            <option value="cancelled" ${apt.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
                        </select>
                    </td>
                    <td><button onclick="deleteAppointment(${apt.id})">Delete</button></td>
                </tr>
            `).join('');
        }

        function updateStats(appointments) {
            const total = appointments.length;
            const pending = appointments.filter(a => a.status === 'pending').length;
            const confirmed = appointments.filter(a => a.status === 'confirmed').length;
            const revenue = appointments.reduce((sum, a) => sum + a.total, 0);
            
            document.getElementById('total').textContent = total;
            document.getElementById('pending-count').textContent = pending;
            document.getElementById('confirmed-count').textContent = confirmed;
            document.getElementById('revenue').textContent = '₹' + revenue.toFixed(2);
        }

        async function updateStatus(id, status) {
            try {
                const response = await fetch(`http://localhost:5001/api/appointments/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status })
                });
                if (response.ok) {
                    loadAppointments();
                }
            } catch (error) {
                console.error('Error updating status:', error);
            }
        }

        function deleteAppointment(id) {
            if (confirm('Are you sure you want to delete this appointment?')) {
                fetch(`http://localhost:5001/api/appointments/${id}`, {
                    method: 'DELETE'
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert('Appointment deleted successfully');
                        loadAppointments();
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete appointment');
                });
            }
        }

        // Load appointments on page load
        loadAppointments();
        // Refresh every 30 seconds
        setInterval(loadAppointments, 30000);
    </script>
</body>
</html>
'''

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to view all appointments"""
    return render_template_string(ADMIN_DASHBOARD)

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📊 Admin Dashboard (Local): http://localhost:5001/admin")
    print("📊 Admin Dashboard (Network): http://<YOUR_IP>:5001/admin")
    print("📝 API endpoint: http://localhost:5001/api/appointments")
    print("\nTo find your IP address, run: ipconfig getifaddr en0")
    app.run(debug=True, host='0.0.0.0', port=5001)
