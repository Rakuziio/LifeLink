from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import User, BloodBank, BloodRequest, BloodStock
from app.utils.decorators import admin_required
from app.extensions import db
from flask_login import current_user
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin_dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/users')
@admin_required
def users():
    
    role = request.args.get('role')
    is_verified = request.args.get('is_verified')
    is_donor = request.args.get('is_donor')

    #filter
    filters = []

    # convert string → boolean
    if is_verified is not None:
        is_verified = is_verified.lower() == 'true'

    if is_donor is not None:
        is_donor = is_donor.lower() == 'true'

    #Build filter
    if role:
        filters.append(User.role == role)
    if is_verified is not None:
        filters.append(User.is_verified == is_verified)
    if is_donor is not None:
        filters.append(User.is_donor == is_donor)

    # or filter
    if filters:
        users = User.query.filter(or_(*filters)).all()
    else:
        users = User.query.all()
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/bloodbanks')
@admin_required
def bloodbanks():
    banks = BloodBank.query.all()
    return render_template('admin/bloodbanks.html', banks=banks)


@admin_bp.route('/requests')
@admin_required
def requests():
    requests = BloodRequest.query.all()
    return render_template('admin/requests.html', requests=requests)


@admin_bp.route('/stock')
@admin_required
def stock():
    stock = BloodStock.query.all()
    return render_template('admin/stock.html', stock=stock)


# DELETE USER
@admin_bp.route('/delete/<int:user_id>')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    if user.id == current_user.id:
        flash("You can't delete yourself!", "warning")
    flash("User deleted permanently", "danger")
    return redirect(url_for('admin.users'))
