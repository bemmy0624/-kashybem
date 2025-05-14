from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key_here'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kate"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        cursor.execute("INSERT INTO employees (name, position, email) VALUES (%s, %s, %s)", (name, position, email))
        db.commit()
        flash("Employee added!", "success")
        return redirect(url_for('view_employees'))
    return render_template('add_employee.html')

@app.route('/update-employee/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        cursor.execute("UPDATE employees SET name=%s, position=%s, email=%s WHERE id=%s", (name, position, email, id))
        db.commit()
        flash("Employee updated!", "info")
        return redirect(url_for('view_employees'))
    return render_template('update_employee.html', employee=employee)

@app.route('/employees')
def view_employees():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    search = request.args.get('search')
    if search:
        cursor.execute("SELECT * FROM employees WHERE name LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('view_employees.html', employees=employees)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        status = request.form['status']
        cursor.execute("INSERT INTO attendance (employee_id, status) VALUES (%s, %s)", (emp_id, status))
        db.commit()
        flash("Attendance recorded!", "success")
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('attendance.html', employees=employees)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
