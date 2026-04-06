from app.extensions import db
from datetime import date

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(5), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(15), unique=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)