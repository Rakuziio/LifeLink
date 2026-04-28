from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='nuser')
    is_verified = db.Column(db.Boolean, default=False)
    is_donor = db.Column(db.Boolean, default=False)

    donor = db.relationship("Donor", backref="user")

class BloodRequest(db.Model):
    __tablename__ = "blood_requests"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bloodbank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.id'))

    blood_type = db.Column(db.String(5))
    quantity_ml = db.Column(db.Integer)

    patient_name = db.Column(db.String(100))
    hospital_name = db.Column(db.String(200))

    status = db.Column(db.String(20), default="pending")  
    # pending / approved / rejected / completed

    request_date = db.Column(db.DateTime, default=db.func.current_timestamp())