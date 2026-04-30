from app.extensions import db
from datetime import datetime, timezone

class BloodBank(db.Model):
    __tablename__ = "blood_banks"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='bloodbank')
    stock = db.relationship('BloodStock', backref='bloodbank', lazy=True)
    
    state = db.Column(db.String(20), nullable=False)
    district = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    helpline_number = db.Column(db.String(15))
    license_number = db.Column(db.String(100), nullable=False)

class BloodStock(db.Model):
    __tablename__ = "blood_stock"

    __table_args__ = (
        db.UniqueConstraint('bloodbank_id', 'blood_type', name='unique_blood_per_bank'),
    )
    
    id = db.Column(db.Integer, primary_key=True)

    bloodbank_id = db.Column(db.Integer, db.ForeignKey('blood_banks.id'))

    blood_type = db.Column(db.String(5))
    quantity_ml = db.Column(db.Integer, default=0)
