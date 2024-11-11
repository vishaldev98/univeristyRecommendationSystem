from base import db
from base.com.vo.prediction_vo import PredictionVO


class PredictionDAO:
    def insert_prediction(self, prediction_vo):
        db.session.add(prediction_vo)
        db.session.commit()

    def view_prediction(self, prediction_vo):
        prediction_vo_list = PredictionVO.query.filter_by(prediction_login_id=prediction_vo.prediction_login_id).all()
        print("prediction_vo_list=",prediction_vo_list)
        return prediction_vo_list
