from flask import request, render_template, url_for, redirect, jsonify

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.dao.universitydetails_dao import UniversityDetailsDAO
from base.com.dao.universityinfo_dao import UniversityInfoDAO
from base.com.vo.department_vo import DepartmentVO
from base.com.vo.universitydetails_vo import UniversityDetailsVO


@app.route('/admin/load_universitydetails')
def admin_load_universitydetails():
    try:
        if admin_login_session() == "admin":
            universityinfo_dao = UniversityInfoDAO()
            universityinfo_vo_list = universityinfo_dao.view_universityinfo()
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            return render_template('admin/addUniversityDetails.html', degree_vo_list=degree_vo_list,
                                   universityinfo_vo_list=universityinfo_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/ajax_department_universitydetails')
def admin_ajax_department_universitydetails():
    try:
        if admin_login_session() == "admin":
            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_degree_id = request.args.get('universityDetailsDegreeId')
            department_vo.department_degree_id = department_degree_id
            department_vo_list = department_dao.view_ajax_department_universitydetails(department_vo)
            ajax_universityDetails_department = [i.as_dict() for i in department_vo_list]
            return jsonify(ajax_universityDetails_department)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_ajax_department_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_universitydetails', methods=['POST'])
def admin_insert_universitydetails():
    try:
        if admin_login_session() == "admin":
            universitydetails_universityinfo_id = request.form.get('universityDetailsUniversityInfoId')
            universitydetails_degree_id = request.form.get('universityDetailsDegreeId')
            universitydetails_department_id = request.form.get('universityDetailsDepartmentId')
            universitydetails_cutoff = request.form.get('universityDetailsCutOff')
            universitydetails_ielts_score = request.form.get('universityDetailsIelts')
            universitydetails_gre_score = request.form.get('universityDetailsGre')

            universitydetails_vo = UniversityDetailsVO()
            universitydetails_dao = UniversityDetailsDAO()

            universitydetails_vo.universitydetails_cutoff = universitydetails_cutoff
            universitydetails_vo.universitydetails_ielts_score = universitydetails_ielts_score
            universitydetails_vo.universitydetails_gre_score = universitydetails_gre_score
            universitydetails_vo.universitydetails_universityinfo_id = universitydetails_universityinfo_id
            universitydetails_vo.universitydetails_degree_id = universitydetails_degree_id
            universitydetails_vo.universitydetails_department_id = universitydetails_department_id
            universitydetails_dao.insert_universitydetails(universitydetails_vo)
            return redirect(url_for('admin_view_universitydetails'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_universitydetails')
def admin_view_universitydetails():
    try:
        if admin_login_session() == "admin":
            universitydetails_dao = UniversityDetailsDAO()
            universitydetails_vo_list = universitydetails_dao.view_universitydetails()
            print(">>>>>>>>>>>>>>>", universitydetails_vo_list)
            return render_template('admin/viewUniversityDetails.html',
                                   universitydetails_vo_list=universitydetails_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_universitydetails', methods=['GET'])
def admin_delete_universitydetails():
    try:
        if admin_login_session() == "admin":
            universitydetails_vo = UniversityDetailsVO()
            universitydetails_dao = UniversityDetailsDAO()
            universitydetails_id = request.args.get('universityDetailsId')
            universitydetails_vo.universitydetails_id = universitydetails_id
            universitydetails_dao.delete_universitydetails(universitydetails_vo)
            return redirect('/admin/view_universitydetails')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_universitydetails', methods=['GET'])
def admin_edit_universitydetails():
    try:
        if admin_login_session() == "admin":
            universitydetails_vo = UniversityDetailsVO()
            universitydetails_dao = UniversityDetailsDAO()

            universityinfo_dao = UniversityInfoDAO()
            universityinfo_vo_list = universityinfo_dao.view_universityinfo()
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()

            universitydetails_id = request.args.get('universityDetailsId')
            universitydetails_vo.universitydetails_id = universitydetails_id
            universitydetails_vo_list = universitydetails_dao.edit_universitydetails(universitydetails_vo)
            return render_template('admin/editUniversityDetails.html',
                                   universitydetails_vo_list=universitydetails_vo_list,
                                   universityinfo_vo_list=universityinfo_vo_list, degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_universitydetails route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_universitydetails', methods=['POST'])
def admin_update_universitydetails():
    try:
        if admin_login_session() == "admin":
            universitydetails_id = request.form.get('universityDetailsId')
            universitydetails_universityinfo_id = request.form.get('universityDetailsUniversityInfoId')
            universitydetails_degree_id = request.form.get('universityDetailsDegreeId')
            universitydetails_department_id = request.form.get('universityDetailsDepartmentId')
            universitydetails_cutoff = request.form.get('universityDetailsCutOff')
            universitydetails_ielts_score = request.form.get('universityDetailsIelts')
            universitydetails_gre_score = request.form.get('universityDetailsGre')

            universitydetails_vo = UniversityDetailsVO()
            universitydetails_dao = UniversityDetailsDAO()

            universitydetails_vo.universitydetails_id = universitydetails_id
            universitydetails_vo.universitydetails_cutoff = universitydetails_cutoff
            universitydetails_vo.universitydetails_ielts_score = universitydetails_ielts_score
            universitydetails_vo.universitydetails_gre_score = universitydetails_gre_score
            universitydetails_vo.universitydetails_universityinfo_id = universitydetails_universityinfo_id
            universitydetails_vo.universitydetails_degree_id = universitydetails_degree_id
            universitydetails_vo.universitydetails_department_id = universitydetails_department_id
            universitydetails_dao.update_universitydetails(universitydetails_vo)
            return redirect('/admin/view_universitydetails')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_universitydetails route exception occured>>>>>>>>>>", ex)
