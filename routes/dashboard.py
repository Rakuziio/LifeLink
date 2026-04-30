from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.bloodbanks import BloodBank
from models.bloodbanks import BloodStock
from models.user import BloodRequest, User
from app.extensions import db
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/bloodbank_dashboard", methods = ['GET', 'POST'])
@login_required
def dashboard_page():
    bloodbank = BloodBank.query.filter_by(user_id=current_user.id).first()

    total_users = User.query.count()
    total_donors = User.query.filter_by(is_donor=True).count()
    total_bloodbanks = BloodBank.query.count()

    total_requests = BloodRequest.query.filter_by(bloodbank_id=bloodbank.id).count()
    pending_requests = BloodRequest.query.filter_by(
        bloodbank_id=bloodbank.id, status='pending'
    ).count()

    approved_requests = BloodRequest.query.filter_by(
        bloodbank_id=bloodbank.id, status='approved'
    ).count()

    rejected_requests = BloodRequest.query.filter_by(
        bloodbank_id=bloodbank.id, status='rejected'
    ).count()

    cancelled_requests = BloodRequest.query.filter_by(
        bloodbank_id=bloodbank.id, status='cancelled'
    ).count()

    completed_requests = BloodRequest.query.filter_by(
        bloodbank_id=bloodbank.id, status='completed'
    ).count()

    return render_template(
        'bloodbank_dashboard.html',
        bloodbank=bloodbank,
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

@dashboard_bp.route("/bloodbank_requests", methods = ['GET', 'POST'])
@login_required
def bloodbank_requests():
    user_id = current_user.id

    if not user_id:
        return redirect(url_for('auth.login'))

    bloodbank = BloodBank.query.filter_by(user_id=user_id).first()
    requests = BloodRequest.query.filter_by(bloodbank_id=bloodbank.id).all()

    if request.method == 'POST':
        request_id = request.form.get('request_id')
        status = request.form.get('status')

        req = BloodRequest.query.get(request_id)
        req.status = status

        db.session.commit()

    return render_template('bloodbank_requests.html', bloodbank=bloodbank, requests=requests)


@dashboard_bp.route("/bloodbank_stock", methods = ['GET', 'POST'])
@login_required
def bloodbank_stock():
    bloodbank = BloodBank.query.filter_by(user_id=current_user.id).first()

    bank_id = bloodbank.id
    stock_list = BloodStock.query.filter_by(bloodbank_id=bank_id).all()
    return render_template('bloodbank_stock.html', stock=stock_list, bloodbank=bloodbank)


@dashboard_bp.route('/add_blood_stock', methods=['POST'])
@login_required
def add_blood_stock():

    bloodbank = BloodBank.query.filter_by(user_id=current_user.id).first()

    blood_type = request.form.get('blood_type')
    quantity = int(request.form.get('quantity_ml'))

    if quantity < 0:
        return "Quantity must be positive", 400
    
    stock = BloodStock.query.filter_by(
        bloodbank_id=bloodbank.id,
        blood_type=blood_type
    ).first()

    if stock:
        # update existing
        stock.quantity_ml += quantity
    else:
        # create new
        new_stock = BloodStock(
            bloodbank_id=bloodbank.id,
            blood_type=blood_type,
            quantity_ml=quantity
        )
        db.session.add(new_stock)

    db.session.commit()

    return redirect("/bloodbank_stock")


@dashboard_bp.route('/reduce_blood_stock', methods=['POST'])
@login_required
def reduce_blood_stock():
    bloodbank = BloodBank.query.filter_by(user_id=current_user.id).first()

    if not bloodbank:
        return "Blood Bank Not Found", 404
    
    blood_type = request.form.get('blood_type')
    quantity = int(request.form.get('quantity_ml'))

    stock = BloodStock.query.filter_by(
        bloodbank_id=bloodbank.id,
        blood_type=blood_type
    ).first()

    if stock:
        stock.quantity_ml = max(0, stock.quantity_ml - quantity)  # no negative

    db.session.commit()
    return redirect("/bloodbank_stock")


@dashboard_bp.route('/update_blood_stock', methods=['POST'])
@login_required
def update_blood_stock():
    bloodbank = BloodBank.query.filter_by(user_id=current_user.id).first()

    if not bloodbank:
        return "Blood Bank Not Found", 404
    
    blood_type = request.form.get('blood_type')
    quantity = int(request.form.get('quantity_ml'))

    stock = BloodStock.query.filter_by(
        bloodbank_id=bloodbank.id,
        blood_type=blood_type
    ).first()

    if stock:
        stock.quantity_ml = quantity   # overwrite
    else:
        new_stock = BloodStock(
            bloodbank_id=bloodbank.id,
            blood_type=blood_type,
            quantity_ml=quantity
        )
        db.session.add(new_stock)

    db.session.commit()
    return redirect(url_for('dashboard.bloodbank_stock'))