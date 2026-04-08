from app.extensions import db
from datetime import datetime

class DonorHealth(db.Model):
    __tablename__ = "donor_health"
    
    id = db.Column(db.Integer, primary_key=True)

    #permanent health cases
    has_hiv = db.Column(db.Boolean, nullable=False, default=False)
    has_hepatitis_b = db.Column(db.Boolean, nullable=False, default=False)
    has_hepatitis_c = db.Column(db.Boolean, nullable=False, default=False)

    #temporary health cases
    has_syphilis = db.Column(db.Boolean, nullable=False, default=False)
    has_malaria = db.Column(db.Boolean, nullable=False, default=False)
    has_diabetes = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False, unique=True)
    