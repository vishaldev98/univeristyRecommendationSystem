import warnings

import pandas as pd
from flask import request, render_template,redirect
from six import print_

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.controller.test_australia_prediction import perform_university_prediction_australia
from base.com.controller.test_canada_prediction import perform_university_prediction_canada
from base.com.controller.test_usa_prediction import perform_university_prediction_usa
from base.com.dao.login_dao import LoginDAO
from base.com.dao.prediction_dao import PredictionDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.prediction_vo import PredictionVO

warnings.filterwarnings('ignore')


@app.route('/user/load_prediction')
def user_load_prediction():
    try:
        if admin_login_session() == "user":
            return render_template('user/addPrediction.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_load_prediction route exception occured>>>>>>>>>>", ex)


@app.route('/user/insert_prediction', methods=['POST'])
def user_insert_prediction():
    try:
        if admin_login_session() == "user":
            prediction_gre_score = request.form.get("predictionGre")
            prediction_ielts_score = request.form.get('predictionIelts')
            prediction_gpa_score = request.form.get('predictionGpaScore')
            prediction_toefl_score = request.form.get('predictionToefl')
            prediction_passout_year = request.form.get('predictionPassOutYear')
            prediction_work_experience = request.form.get('predictionWorkExperience')
            prediction_internship_month = request.form.get('predictionInternshipMonth')
            prediction_research_paper = request.form.get('predictionResearchPaper')
            prediction_conference_attend = request.form.get('predictionConferenceAttend')
            prediction_country = request.form.get('predictionCountry')


            prediction_gre_score = int(prediction_gre_score)
            prediction_ielts_score = float(prediction_ielts_score)
            prediction_gpa_score = float(prediction_gpa_score)
            prediction_toefl_score = float(prediction_toefl_score)
            prediction_passout_year = int(prediction_passout_year)
            prediction_work_experience = int(prediction_work_experience)
            prediction_internship_month = int(prediction_internship_month)
            prediction_research_paper = int(prediction_research_paper)
            prediction_conference_attend = int(prediction_conference_attend)

            prediction_vo = PredictionVO()
            prediction_dao = PredictionDAO()

            if prediction_country == 'USA':
                column_value = [prediction_gre_score, prediction_ielts_score, prediction_gpa_score,
                                prediction_toefl_score, prediction_passout_year,
                                prediction_work_experience, prediction_internship_month,
                                prediction_research_paper, prediction_conference_attend]
                column_name = ['GRE', 'IELTS', 'GPA', 'TOFEL', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                               'ResearchPaper', 'ConferenceAttend']
                df = pd.DataFrame([column_value], columns=column_name)
                prediction_university = perform_university_prediction_usa(df)
                print("Prediction for USA:", prediction_university)
                if not prediction_university:
                    prediction_university = "No prediction available"
                prediction_vo.prediction_university = prediction_university

            elif prediction_country == 'Canada':
                column_value = [prediction_gre_score, prediction_ielts_score,
                                prediction_gpa_score, prediction_passout_year,
                                prediction_work_experience, prediction_internship_month,
                                prediction_research_paper, prediction_conference_attend]
                column_name = ['GRE', 'IELTS', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                               'ResearchPaper', 'ConferenceAttend']
                df = pd.DataFrame([column_value], columns=column_name)
                prediction_university = perform_university_prediction_canada(df)
                prediction_vo.prediction_university = prediction_university

            elif prediction_country == 'Australia':
                column_value = [prediction_ielts_score, prediction_toefl_score,
                                prediction_gpa_score, prediction_passout_year,
                                prediction_work_experience, prediction_internship_month,
                                prediction_research_paper, prediction_conference_attend]
                column_name = ['IELTS','TOFEL', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                               'ResearchPaper', 'ConferenceAttend']
                df = pd.DataFrame([column_value], columns=column_name)
                prediction_university = perform_university_prediction_australia(df)
                prediction_vo.prediction_university = prediction_university

                if not prediction_university:
                    prediction_university = "No prediction available"
                prediction_vo.prediction_university = prediction_university

            prediction_vo.prediction_gre_score = prediction_gre_score
            prediction_vo.prediction_ielts_score = prediction_ielts_score
            prediction_vo.prediction_gpa_score = prediction_gpa_score
            prediction_vo.prediction_toefl_score = prediction_toefl_score
            prediction_vo.prediction_passout_year = prediction_passout_year
            prediction_vo.prediction_work_experience = prediction_work_experience
            prediction_vo.prediction_internship_month = prediction_internship_month
            prediction_vo.prediction_research_paper = prediction_research_paper
            prediction_vo.prediction_conference_attend = prediction_conference_attend
            prediction_vo.prediction_country = prediction_country

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            prediction_vo.prediction_login_id = login_id

            prediction_dao.insert_prediction(prediction_vo)

            return redirect('/user/view_prediction')

        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_insert_prediction route exception occured>>>>>>>>>>", ex)

@app.route('/user/view_prediction')
def user_view_prediction():
    try:
        if admin_login_session() == "user":

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            prediction_vo = PredictionVO()
            prediction_dao = PredictionDAO()

            prediction_vo.prediction_login_id = login_id

            prediction_vo_list = prediction_dao.view_prediction(prediction_vo)

            return render_template('user/viewPrediction.html',prediction_vo_list=prediction_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print(" user_view_prediction route exception occured>>>>>>>>>>", ex)