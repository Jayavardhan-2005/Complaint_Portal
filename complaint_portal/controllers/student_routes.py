from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from models import User, Complaint
from utils import hash_password, verify_password

student_bp = Blueprint('student', __name__)
mongo = PyMongo()

@student_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and verify_password(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            if user['role'] == 'student':
                return redirect(url_for('student.student_dashboard'))
            else:
                return redirect(url_for('admin.admin_dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@student_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if User.find_by_email(email):
            flash('Email already exists')
        else:
            hashed_password = hash_password(password)
            User.create(email, hashed_password, role)
            flash('Registration successful! Please login.')
            return redirect(url_for('student.login'))
    return render_template('register.html')

@student_bp.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('student.login'))
    user = User.find_by_id(session['user_id'])
    complaints = Complaint.find_by_user_id(session['user_id'])
    return render_template('dashboard_student.html', user=user, complaints=complaints)

@student_bp.route('/student/apply_complaint', methods=['GET', 'POST'])
def apply_complaint():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('student.login'))
    if request.method == 'POST':
        department = request.form['department']
        description = request.form['description']
        Complaint.create(session['user_id'], department, description)
        flash('Complaint registered successfully!')
        return redirect(url_for('student.student_dashboard'))
    return render_template('apply_complaint.html')

@student_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('student.login'))