from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from models import Complaint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('student.login'))
    complaints = Complaint.find_all()
    return render_template('dashboard_admin.html', complaints=complaints)

@admin_bp.route('/admin/view_complaints')
def view_complaints():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('student.login'))
    complaints = Complaint.find_all()
    return render_template('view_complaints.html', complaints=complaints)

@admin_bp.route('/admin/update_complaint/<complaint_id>', methods=['POST'])
def update_complaint(complaint_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('student.login'))
    solution = request.form['solution']
    status = request.form['status']
    department = request.form['department']
    Complaint.update(complaint_id, solution, status, department)
    flash('Complaint updated successfully!')
    return redirect(url_for('admin.admin_dashboard'))