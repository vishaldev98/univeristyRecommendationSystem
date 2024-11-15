from base import db


class UniversityInfoVO(db.Model):
    __tablename__ = 'universityinfo_table'
    universityinfo_id = db.Column('universityinfo_id', db.Integer, primary_key=True, autoincrement=True)
    universityinfo_name = db.Column('universityinfo_name', db.String(100), nullable=False)
    universityinfo_address = db.Column('universityinfo_address', db.String(100), nullable=False)
    universityinfo_fees = db.Column('universityinfo_fees', db.String(100), nullable=False)
    universityinfo_contact = db.Column('universityinfo_contact', db.NUMERIC, nullable=False)
    universityinfo_email = db.Column('universityinfo_email', db.String(100), nullable=False)
    universityinfo_description = db.Column('universityinfo_description', db.String(100), nullable=False)

    def as_dict(self):
        return {
            'universityinfo_id': self.universityinfo_id,
            'universityinfo_name': self.universityinfo_name,
            'universityinfo_address': self.universityinfo_address,
            'universityinfo_fees': self.universityinfo_fees,
            'universityinfo_contact': self.universityinfo_contact,
            'universityinfo_email': self.universityinfo_email,
            'universityinfo_description': self.universityinfo_description
        }


