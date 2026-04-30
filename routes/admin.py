from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import BloodBank, BloodRequest, BloodStock, Donor
from app.utils.decorators import admin_required
from app.extensions import db
from flask_login import current_user
from models.user import User
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin_dashboard')
@admin_required
def dashboard():
    
    total_users = User.query.count()

    total_donors = User.query.filter_by(is_donor=True).count()

    total_bloodbanks = BloodBank.query.count()

    total_requests = BloodRequest.query.count()

    pending_requests = BloodRequest.query.filter_by(status='pending').count()

    approved_requests = BloodRequest.query.filter_by(status='approved').count()

    rejected_requests = BloodRequest.query.filter_by(status='rejected').count()

    cancelled_requests = BloodRequest.query.filter_by(status='cancelled').count()

    completed_requests = BloodRequest.query.filter_by(status='completed').count()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_donors=total_donors,
        total_bloodbanks=total_bloodbanks,
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests,
        cancelled_requests=cancelled_requests,
        completed_requests=completed_requests
    )


@admin_bp.route('/users')
@admin_required
def users():
    
    role = request.args.get('role')
    is_verified = request.args.get('is_verified')
    is_donor = request.args.get('is_donor')

    #filter
    filters = []

    #Build filter
    if role:
        filters.append(User.role == role)
    if is_verified is not None and is_verified != "":
        is_verified_bool = is_verified.lower() == 'true'
        filters.append(User.is_verified == is_verified_bool)
    if is_donor is not None and is_donor != "":
        is_donor_bool = is_donor.lower() == 'true'
        filters.append(User.is_donor == is_donor_bool)

    # or filter
    if filters:
        users = User.query.filter(or_(*filters)).all()
    else:
        users = User.query.all()
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/donors')
@admin_required
def donors():
    state = request.args.get('state')
    district = request.args.get('district')
    availability = request.args.get('availability')

    # START query
    query = Donor.query

    if state:
        query = query.filter(Donor.state == state)

    if district:
        query = query.filter(Donor.district == district)

    if availability == 'true':
        query = query.filter(Donor.availability == True)
    elif availability == 'false':
        query = query.filter(Donor.availability == False)

    # EXECUTE query
    donors = query.all()

    return render_template(
        'admin/donors.html',
        donors=donors,
        selected_state=state,
        selected_district=district,
        selected_availability=availability
    )


@admin_bp.route('/bloodbanks')
@admin_required
def bloodbanks():
    state = request.args.get('state')
    district = request.args.get('district')
    is_verified = request.args.get('is_verified')

    query = BloodBank.query.join(User)

    if state:
        query = query.filter_by(state=state)

    if district:
        query = query.filter_by(district=district)

    if is_verified:
        if is_verified == 'true':
            query = query.filter(User.is_verified == True)
        elif is_verified == 'false':
            query = query.filter(User.is_verified == False)

    bloodbanks = query.all()

    return render_template(
        'admin/bloodbanks.html',
        bloodbanks=bloodbanks,
        selected_state=state,
        selected_district=district,
        selected_verified=is_verified
    )


@admin_bp.route('/requests')
@admin_required
def requests():
    
    status = request.args.get('status')

    #filter
    if status:
        requests = BloodRequest.query.filter_by(
            status=status,
        ).all()
    else:
        requests = BloodRequest.query.all()

    return render_template('admin/requests.html', requests=requests)


@admin_bp.route('/stock')
@admin_required
def stock():
    bank_id = request.args.get('bloodbanks_id')

    #filter
    if bank_id:
        stock = BloodStock.query.filter_by(bloodbank_id=bank_id).all()
    else:
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

# DELETE DONOR
@admin_bp.route('/delete/<int:donor_id>')
@admin_required
def delete_donor(donor_id):
    donor = User.query.get_or_404(donor_id)
    db.session.delete(donor)
    db.session.commit()
    flash("Donor deleted permanently", "danger")
    return redirect(url_for('admin.donors'))

# DELETE REQUESTS
@admin_bp.route('/delete/<int:requests_id>')
@admin_required
def delete_request(requests_id):
    request = User.query.get_or_404(requests_id)
    db.session.delete(request)
    db.session.commit()
    flash("Request deleted permanently", "danger")
    return redirect(url_for('admin.requests'))

# DELETE BLOOD BANKS
@admin_bp.route('/delete/<int:bloodbanks_id>')
@admin_required
def delete_bloodbank(bloodbanks_id):
    bloodbank = User.query.get_or_404(bloodbanks_id)
    db.session.delete(bloodbank)
    db.session.commit()
    flash("Blood bank deleted permanently", "danger")
    return redirect(url_for('admin.bloodbanks'))

# VERIFY BLOOD BANKS
@admin_bp.route('/verify-bloodbank/<int:user_id>', methods=['POST'])
@admin_required
def verify_bloodbank(user_id):
    user = User.query.get_or_404(user_id)

    if user.role == 'blood_bank':
        user.is_verified = not user.is_verified
        db.session.commit()

    return redirect(url_for('admin.users'))