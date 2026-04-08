from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.donor import Donor
from models.donor_health import DonorHealth

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
@home_bp.route("/home")
def home_page():
    return render_template('home.html')

@home_bp.route("/profile")
@login_required
def profile_page():
    donor = None
    health = None

    if current_user.is_donor:
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        if donor:
            health = DonorHealth.query.filter_by(donor_id=donor.id).first()
    return render_template('profile.html', user=current_user, donor=donor, health = health)