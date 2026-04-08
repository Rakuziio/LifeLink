from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from models.donor import Donor
from models.donor_health import DonorHealth
from datetime import datetime

donor_bp = Blueprint('donor', __name__)

@donor_bp.route("/become-donor", methods=['GET', 'POST'])
@login_required
def become_donor():
    if current_user.is_donor:
        flash("You are already registered as a Donor.", category='info')
        return redirect(url_for('home_bp.home_page'))

    if request.method=='POST':
        blood_type=request.form.get('blood_type')
        dob=datetime.strptime(request.form.get('dob'), "%Y-%m-%d").date()
        state=request.form.get('state')
        city=request.form.get('city')
        gender=request.form.get('gender')
        phone=request.form.get('phone')

        #creating new donor object
        new_donor = Donor(
            user_id = current_user.id,
            blood_type=blood_type,
            dob=dob,
            state=state,
            city=city,
            gender=gender,
            phone=phone
        )

        if new_donor.age<18:
            flash('An individual below age 18 are not recommended to donate blood', category='error')
        elif new_donor.age>65:
            flash('An individual above age 65 are not recommended to donate blood', category='error')

        current_user.is_donor = True

        db.session.add(current_user)
        db.session.add(new_donor)
        db.session.commit()

        flash('Congratulation!!! You are now a LifeLink community', category='success')
        return redirect(url_for('home.home_page'))

    return render_template('donor_signup.html')


@donor_bp.route("/donor")
def donor_page():
    return render_template('donor.html')

@donor_bp.route("/donor-health", methods=['GET', 'POST'])
@login_required
def donor_health():
    if current_user.is_donor:
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        health = DonorHealth.query.filter_by(donor_id=donor.id).first()

        if request.method == "POST":
            has_hiv = request.form.get("has_hiv") =="yes"
            has_hepatitis_b = request.form.get("has_hepatitis_b") == "yes"
            has_hepatitis_c = request.form.get("has_hepatitis_c") == "yes"

            has_syphilis = request.form.get("has_syphilis") == "yes"
            has_malaria = request.form.get("has_malaria") == "yes"
            has_diabetes = request.form.get("has_diabetes") == "yes"

            if health:
                # UPDATE
                health.has_hiv = has_hiv
                health.has_hepatitis_b = has_hepatitis_b
                health.has_hepatitis_c = has_hepatitis_c

                health.has_syphilis = has_syphilis
                health.has_malaria = has_malaria
                health.has_diabetes = has_diabetes
            else:
                # CREATE
                health = DonorHealth(
                    donor_id=donor.id,
                    has_hiv=has_hiv,
                    has_hepatitis_b=has_hepatitis_b,
                    has_hepatitis_c=has_hepatitis_c,

                    has_syphilis=has_syphilis,
                    has_malaria=has_malaria,
                    has_diabetes=has_diabetes
                )
                db.session.add(health)
            db.session.commit()
            return redirect(url_for('home.profile_page'))


    return render_template('profile.html', health = health)