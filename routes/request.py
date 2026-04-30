from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.bloodbanks import BloodBank
from models.bloodbanks import BloodStock
from models.user import User
from models.user import BloodRequest
from app.extensions import db
from flask_login import login_required, current_user

request_bp = Blueprint('request', __name__)

@request_bp.route("/request_page", methods = ['GET', 'POST'])
@login_required
def request_page():

    state = request.args.get('state')
    district = request.args.get('district')

    #filter
    if state and district:
        bloodbanks = BloodBank.query.filter_by(
            state=state,
            district=district
        ).all()
    else:
        bloodbanks = BloodBank.query.all()

    return render_template('request.html', bloodbanks=bloodbanks)

@request_bp.route('/send_request', methods=['POST'])
@login_required
def send_request():
    patient_name = request.form.get('patient_name')
    blood_type = request.form.get('blood_type')
    quantity_ml = request.form.get('units')
    contact = request.form.get('contact')
    bloodbank_id = request.form.get('bloodbank_id')
    hospital_name = request.form.get('hospital_name')

    # save to DB
    new_request = BloodRequest(
        user_id = current_user.id,
        patient_name=patient_name,
        blood_type=blood_type,
        quantity_ml=quantity_ml,
        contact=contact,
        bloodbank_id=bloodbank_id,
        hospital_name=hospital_name
    )

    db.session.add(new_request)
    db.session.commit()

    flash('Requested successfully', category='success')
    return redirect(url_for('home.home_page'))

@request_bp.route('/my_request', methods=['GET'])
@login_required
def my_request():
    requests = BloodRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('my_request.html', requests=requests)