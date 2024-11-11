from base import db
from base.com.vo.country_vo import CountryVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.prediction_vo import PredictionVO


class PredictionDAO:
    def insert_prediction(self, prediciton_vo):
        db.session.add(prediciton_vo)
        db.session.commit()

    def user_view_prediction(self,prediciton_vo):
        prediction_vo_list = db.session.query(PredictionVO,CountryVO)\
            .filter_by(prediction_login_id=prediciton_vo.prediction_login_id)\
            .filter(PredictionVO.prediction_country_id == CountryVO.country_id)\
            .all()
        print("prediction_vo_list=",prediction_vo_list)
        return prediction_vo_list

    def admin_view_prediction(self):
        prediction_vo_list = db.session.query(PredictionVO,CountryVO,LoginVO)\
            .filter(PredictionVO.prediction_country_id == CountryVO.country_id) \
            .filter(PredictionVO.prediction_login_id == LoginVO.login_id) \
            .all()
        print("prediction_vo_list=",prediction_vo_list)
        return prediction_vo_list