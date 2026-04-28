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
    syphilis_cured = db.Column(db.Boolean, nullable=True)
    syphilis_cured_date = db.Column(db.Date, nullable=True)

    has_malaria = db.Column(db.Boolean, nullable=False, default=False)
    malaria_cured = db.Column(db.Boolean, nullable=True)
    malaria_cured_date = db.Column(db.Date, nullable=True)

    has_diabetes = db.Column(db.Boolean, nullable=False, default=False)


    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False, unique=True)
    
    def check_eligibility(health):
        # Permanent rejection
        if health.has_hiv:
            return "Not Eligible"

        # Temporary rejection - malaria
        if health.has_malaria:
            if not health.malaria_cured:
                return "Not Eligible (Temporary)"

            # If cured, check recovery time (example: 3 months)
            if health.malaria_cured_date:
                from datetime import datetime, timedelta
                eligible_date = health.malaria_cured_date + timedelta(days=90)

                if datetime.utcnow() < eligible_date:
                    return "Not Eligible (Temporary)"

        return "Eligible"