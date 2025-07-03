from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secretkey123'

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aman@2698',
    database='battery_swap'
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username.lower() == 'admin':  
            return "You cannot register with the username 'admin'. It is reserved for system admin."
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                       (request.form['username'], request.form['password']))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (request.form['username'], request.form['password']))
        user = cursor.fetchone()
        if user:
            session['username'] = user['username']
            return redirect('/dashboard')
        return "Login failed"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    cursor.execute("SELECT * FROM bookings WHERE username=%s", (session['username'],))
    bookings = cursor.fetchall()
    return render_template('dashboard.html', user=session['username'], bookings=bookings)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        cursor.execute("INSERT INTO bookings (username, station, date, status) VALUES (%s, %s, %s, %s)",
                       (session['username'], request.form['station'], request.form['date'], 'Pending'))
        db.commit()
        return redirect('/dashboard')
    return render_template('book.html')

@app.route('/admin')
def admin():
    if session.get('username') != 'Admin':
        return redirect('/')
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    return render_template('admin.html', bookings=bookings)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'Admin' and password == 'Admin_1234':
            session['username'] = 'Admin'
            return redirect('/admin')
        else:
            return "Invalid admin credentials"
    
    return render_template('admin_login.html')

@app.route('/approve-booking/<int:id>', methods=['POST'])
def approve_booking(id):
    if session.get('username') != 'Admin':
        return "Access Denied"
    cursor.execute("UPDATE bookings SET status = 'Approved' WHERE id = %s", (id,))
    db.commit()
    return redirect('/admin')

@app.route('/delete-booking/<int:id>', methods=['POST'])
def delete_booking(id):
    if session.get('username') != 'Admin':
        return "Access Denied"
    cursor.execute("DELETE FROM bookings WHERE id = %s", (id,))
    db.commit()
    return redirect('/admin')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
