from base import db


class CountryVO(db.Model):
    __tablename__ = 'country_table'
    country_id = db.Column('country_id', db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column('country_name', db.String(255), nullable=False)
    country_description = db.Column('country_description', db.String(255), nullable=False)

    def as_dict(self):
        return {
            'country_id': self.country_id,
            'country_name': self.country_name,
            'country_description': self.country_description
        }