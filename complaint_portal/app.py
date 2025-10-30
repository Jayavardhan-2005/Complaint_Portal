from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something more secure for production

# MongoDB connection
client = MongoClient("")
db = client['complaint_portal']  # Your database name
users_collection = db['users']  # Collection for storing user data
complaints_collection = db['complaints']  # Collection for storing complaints


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            flash('Email already registered!')
            return redirect(url_for('register'))

        # Save new user
        users_collection.insert_one({
            'email': email,
            'password': password,  # Plain text for simplicity (not secure in real apps)
            'role': role
        })

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists and password matches
        user = users_collection.find_one({'email': email})
        if user and user['password'] == password:
            session['user_id'] = str(user['_id'])  # Store user ID in session
            session['role'] = user['role']  # Store role in session
            session['email'] = user['email']  # Store email in session

            if user['role'] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))

    return render_template('login.html')


# Student Dashboard route
@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    complaints = list(complaints_collection.find({'user_id': user_id}))
    return render_template('dash_stud.html', user=user, complaints=complaints)


# Admin Dashboard route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    all_complaints = complaints_collection.find()
    return render_template('dash_admin.html', complaints=all_complaints)


# Apply Complaint route (for students)
@app.route('/apply_complaint', methods=['GET', 'POST'])
def apply_complaint():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        department = request.form['department']
        description = request.form['description']

        complaints_collection.insert_one({
            'user_id': session['user_id'],
            'department': department,
            'description': description,
            'status': 'Pending',  # Default status
            'solution': ''
        })

        flash('Complaint registered successfully.')
        return redirect(url_for('student_dashboard'))

    return render_template('apply_comp.html')

@app.route('/view_complaints')
def view_complaints():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    complaints = list(complaints_collection.find())
    return render_template('view_comp.html', complaints=complaints)

from bson.objectid import ObjectId

@app.route('/update_complaint/<complaint_id>', methods=['POST'])
def update_complaint(complaint_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    status = request.form.get('status')
    solution = request.form.get('solution')

    complaints_collection.update_one(
        {'_id': ObjectId(complaint_id)},
        {'$set': {'status': status, 'solution': solution}}
    )

    flash('Complaint updated successfully.')
    return redirect(url_for('view_complaints'))


# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

