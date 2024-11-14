from base import db


class RequestPredictionVO(db.Model):
    __tablename__ = 'prediction_table'
    prediction_id = db.Column('prediction_id', db.Integer, primary_key=True, autoincrement=True)
    prediction_gre_score = db.Column('prediction_gre_score', db.String(15), nullable=False)
    prediction_ielts_score = db.Column('prediction_ielts_score', db.String(15), nullable=False)
    prediction_gpa_score = db.Column('prediction_gpa_score', db.String(15), nullable=False)
    prediction_toefl_score = db.Column('prediction_toefl_score', db.String(15), nullable=False)
    prediction_passout_year = db.Column('prediction_passout_year', db.String(15), nullable=False)
    prediction_work_experience = db.Column('prediction_work_experience', db.String(15), nullable=False)
    prediction_internship_month = db.Column('prediction_internship_month', db.String(15), nullable=False)
    prediction_research_paper = db.Column('prediction_research_paper', db.String(15), nullable=False)
    prediction_conference_attend = db.Column('prediction_conference_attend', db.String(15), nullable=False)

    def as_dict(self):
        return {
            'prediction_id': self.prediction_id,
            'prediction_gre_score': self.prediction_gre_score,
            'prediction_ielts_score': self.prediction_ielts_score,
            'prediction_gpa_score': self.prediction_gpa_score,
            'prediction_toefl_score': self.prediction_toefl_score,
            'prediction_passout_year': self.prediction_passout_year,
            'prediction_work_experience': self.prediction_work_experience,
            'prediction_internship_month': self.prediction_internship_month,
            'prediction_research_paper': self.prediction_research_paper,
            'prediction_conference_attend': self.prediction_conference_attend
        }


db.create_all()