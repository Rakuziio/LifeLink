from app.extensions import db
from datetime import datetime, timezone

class BloodBank(db.Model):
    __tablename__ = "blood_banks"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    helpline_number = db.Column(db.String(15))
    license_number = db.Column(db.String(50))

    has_hospital = db.Column(db.Boolean, nullable=False)
    hospital_name = db.Column(db.String(200), nullable=True)

class BloodStock(db.Model):
    __tablename__ = "blood_stock"

    id = db.Column(db.Integer, primary_key=True)

    bloodbank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.id'))
    blood_type = db.Column(db.String(5))
    quantity_ml = db.Column(db.Integer, default=0)