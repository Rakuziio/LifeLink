from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.donor import Donor

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
@home_bp.route("/home")
def home_page():
    return render_template('home.html')

@home_bp.route("/profile")
@login_required
def profile_page():
    donor = Donor.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', user=current_user, donor=donor)