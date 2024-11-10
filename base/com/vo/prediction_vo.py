from base import db
from base.com.vo.country_vo import CountryVO
from base.com.vo.login_vo import LoginVO


class PredictionVO(db.Model):
    __tablename__ = 'prediction_table'
    prediction_id = db.Column('prediction_id', db.Integer, primary_key=True, autoincrement=True)
    prediction_login_id = db.Column('prediction_login_id', db.Integer, db.ForeignKey(LoginVO.login_id))
    prediction_country_id = db.Column('prediction_country_id', db.Integer, db.ForeignKey(CountryVO.country_id))
    prediction_universityname = db.Column('prediction_universityname', db.String(255), nullable=False)
    prediction_datetime = db.Column('prediction_datetime', db.DateTime)
    prediction_ieltsscore = db.Column('prediction_ieltsscore', db.Float, nullable=False)
    prediction_tofelscore = db.Column('prediction_tofelscore', db.Integer, nullable=False)
    prediction_grescore = db.Column('prediction_grescore', db.Integer, nullable=False)
    prediction_gpascore = db.Column('prediction_gpascore', db.Float, nullable=False)
    prediction_internshipmonths = db.Column('prediction_internshipmonths', db.Integer, nullable=False)
    prediction_passoutyear = db.Column('prediction_passoutyear', db.Integer, nullable=False)
    prediction_workexperience = db.Column('prediction_workexperience', db.Integer, nullable=False)
    prediction_researchpaper = db.Column('prediciton_researchpaper', db.Integer, nullable=False)
    prediction_conferenceattend = db.Column('prediction_conferenceattend', db.Integer, nullable=False)

    def as_dict(self):
        return {
            'prediction_id': self.prediction_id,
            'prediction_login_id': self.prediction_login_id,
            'prediction_universityname': self.prediction_universityname,
            'prediction_datetime': self.prediction_datetime,
            'prediction_country_id': self.prediction_country_id,
            'prediciton_ieltsscore': self.prediction_ieltsscore,
            'prediction_tofelscore': self.prediction_tofelscore,
            'prediction_grescore': self.prediction_grescore,
            'prediction_gpascore': self.prediction_gpascore,
            'prediciton_internshipmonths': self.prediction_internshipmonths,
            'prediction_passoutyear': self.prediction_passoutyear,
            'prediction_workexperience': self.prediction_workexperience,
            'prediciton_researchpaper': self.prediction_researchpaper,
            'prediction_conferenceattend': self.prediction_conferenceattend
        }


db.create_all()