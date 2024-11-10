import datetime

import pandas as pd
from flask import render_template, redirect, request

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.controller.test_australia_prediction import perform_university_prediction_australia
from base.com.controller.test_canada_prediction import perform_university_prediction_canada
from base.com.controller.test_usa_prediction import perform_university_prediction_usa
from base.com.dao.country_dao import CountryDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.prediction_dao import PredictionDAO
from base.com.vo.country_vo import CountryVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.prediction_vo import PredictionVO


@app.route('/admin/view_prediction')
def admin_view_prediciton():
    try:
        if admin_login_session() == "admin":
            prediction_dao = PredictionDAO()
            prediction_vo_list=prediction_dao.admin_view_prediction()
            return render_template('admin/viewPrediction.html',prediction_vo_list=prediction_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_prediction route exception occured>>>>>>>>>>", ex)


@app.route('/user/load_prediction')
def user_load_prediction():
    try:
        if admin_login_session() == "user":

            country_dao = CountryDAO()
            country_vo_list = country_dao.view_country()

            return render_template('user/addPrediction.html', country_vo_list=country_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_load_prediction route exception occured>>>>>>>>>>>>>>>", ex)


@app.route('/user/insert_predicition', methods=['POST'])
def user_insert_predicition():
    try:
        if admin_login_session() == "user":
            country_dao = CountryDAO()
            prediction_date = datetime.datetime.now()
            prediction_country = request.form.get('userCountryname')
            prediction_ielts_score = request.form.get("predictionIelts")
            prediction_toefl_score = request.form.get("predictionTofel")
            prediction_gre_score = request.form.get("predicitionGre")
            prediction_gpa_score = request.form.get("predicitionGpa")
            prediction_internship_month = request.form.get("predictionInternshipmonths")
            prediction_passout_year = request.form.get("predictionPassoutyear")
            prediction_work_experience = request.form.get("predictionWorkexperience")
            prediction_research_paper = request.form.get("predictionResearchpaper")
            prediction_conference_attend = request.form.get("predicitonConferenceattend")

            prediction_gre_score = int(prediction_gre_score)
            prediction_ielts_score = float(prediction_ielts_score)
            prediction_gpa_score = float(prediction_gpa_score)
            prediction_toefl_score = int(prediction_toefl_score)
            prediction_passout_year = int(prediction_passout_year)
            prediction_work_experience = int(prediction_work_experience)
            prediction_internship_month = int(prediction_internship_month)
            prediction_research_paper = int(prediction_research_paper)
            prediction_conference_attend = int(prediction_conference_attend)

            prediction_dao = PredictionDAO()
            prediction_vo = PredictionVO()

            if prediction_country == 'USA':
                column_value = [prediction_gre_score, prediction_ielts_score, prediction_gpa_score,
                                prediction_toefl_score, prediction_passout_year,
                                prediction_work_experience, prediction_internship_month,
                                prediction_research_paper, prediction_conference_attend]
                column_name = ['GRE', 'IELTS', 'GPA', 'TOFEL', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                               'ResearchPaper', 'ConferenceAttend']
                df = pd.DataFrame([column_value], columns=column_name)
                prediction_university = perform_university_prediction_usa(df)
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
                column_name = ['IELTS', 'TOFEL', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                               'ResearchPaper', 'ConferenceAttend']
                df = pd.DataFrame([column_value], columns=column_name)
                prediction_university = perform_university_prediction_australia(df)
                prediction_vo.prediction_university = prediction_university

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            country_vo = CountryVO()
            country_vo.country_name = prediction_country
            country_id = country_dao.find_country(country_vo)

            prediction_vo.prediction_datetime = prediction_date
            prediction_vo.prediction_country_id = country_id
            prediction_vo.prediction_login_id = login_id
            prediction_vo.prediction_universityname = prediction_university
            prediction_vo.prediction_ieltsscore = prediction_ielts_score
            prediction_vo.prediction_tofelscore = prediction_toefl_score
            prediction_vo.prediction_grescore = prediction_gre_score
            prediction_vo.prediction_gpascore = prediction_gpa_score
            prediction_vo.prediction_internshipmonths = prediction_internship_month
            prediction_vo.prediction_passoutyear = prediction_passout_year
            prediction_vo.prediction_workexperience = prediction_work_experience
            prediction_vo.prediction_researchpaper = prediction_research_paper
            prediction_vo.prediction_conferenceattend = prediction_conference_attend
            prediction_dao.insert_prediction(prediction_vo)
            return redirect('/user/view_prediction')

        else:
            return admin_logout_session()
    except Exception as ex:
        print("in user_insert_prediciton route exception occured>>>>>>>>>>", ex)


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
            prediction_vo_list = prediction_dao.user_view_prediction(prediction_vo)

            return render_template('user/viewPrediction.html', prediction_vo_list=prediction_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_view_prediction route exception occured>>>>>>>>>>>>>>>", ex)