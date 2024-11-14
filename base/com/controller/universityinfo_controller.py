from flask import request, render_template, redirect

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.universityinfo_dao import UniversityInfoDAO
from base.com.vo.universityinfo_vo import UniversityInfoVO


@app.route('/admin/load_universityinfo')
def admin_load_universityinfo():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/addUniversityInfo.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_load_universityinfo route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_universityinfo', methods=['POST'])
def admin_insert_universityinfo():
    try:
        if admin_login_session() == "admin":
            universityinfo_name = request.form.get("universityInfoName")
            universityinfo_address = request.form.get("universityInfoAddress")
            universityinfo_fees = request.form.get("universityInfoFees")
            universityinfo_contact = request.form.get("universityInfoContact")
            universityinfo_email = request.form.get("universityInfoEmail")
            universityinfo_description = request.form.get("universityInfoDescription")

            universityinfo_vo = UniversityInfoVO()
            universityinfo_dao = UniversityInfoDAO()

            universityinfo_vo.universityinfo_name = universityinfo_name
            universityinfo_vo.universityinfo_address = universityinfo_address
            universityinfo_vo.universityinfo_fees = universityinfo_fees
            universityinfo_vo.universityinfo_contact = universityinfo_contact
            universityinfo_vo.universityinfo_email = universityinfo_email
            universityinfo_vo.universityinfo_description = universityinfo_description
            universityinfo_dao.insert_universityinfo(universityinfo_vo)
            return redirect('/admin/view_universityinfo')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_insert_universityinfo route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_universityinfo')
def admin_view_universityinfo():
    try:
        if admin_login_session() == "admin":
            universityinfo_dao = UniversityInfoDAO()
            universityinfo_vo_list = universityinfo_dao.view_universityinfo()
            return render_template('admin/viewUniversityInfo.html', universityinfo_vo_list=universityinfo_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_view_universityinfo route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_universityinfo', methods=['GET'])
def admin_delete_universityinfo():
    try:
        if admin_login_session() == "admin":
            universityinfo_vo = UniversityInfoVO()
            universityinfo_dao = UniversityInfoDAO()

            universityinfo_id = request.args.get('universityInfoId')
            universityinfo_vo.universityinfo_id = universityinfo_id
            universityinfo_dao.delete_universityinfo(universityinfo_vo)
            return redirect('/admin/view_universityinfo')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_universityinfo route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_universityinfo', methods=['GET'])
def admin_edit_universityinfo():
    try:
        if admin_login_session() == "admin":
            universityinfo_vo = UniversityInfoVO()
            universityinfo_dao = UniversityInfoDAO()

            universityinfo_id = request.args.get('universityInfoId')
            universityinfo_vo.universityinfo_id = universityinfo_id
            universityinfo_vo_list = universityinfo_dao.edit_universityinfo(universityinfo_vo)
            return render_template('admin/editUniversityInfo.html', universityinfo_vo_list=universityinfo_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_universityinfo route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_universityinfo', methods=['POST'])
def admin_update_universityinfo():
    try:
        if admin_login_session() == "admin":
            universityinfo_id = request.form.get('universityInfoId')
            universityinfo_name = request.form.get("universityInfoName")
            universityinfo_address = request.form.get("universityInfoAddress")
            universityinfo_fees = request.form.get("universityInfoFees")
            universityinfo_contact = request.form.get("universityInfoContact")
            universityinfo_email = request.form.get("universityInfoEmail")
            universityinfo_description = request.form.get("universityInfoDescription")

            universityinfo_vo = UniversityInfoVO()
            universityinfo_dao = UniversityInfoDAO()

            universityinfo_vo.universityinfo_id = universityinfo_id
            universityinfo_vo.universityinfo_name = universityinfo_name
            universityinfo_vo.universityinfo_address = universityinfo_address
            universityinfo_vo.universityinfo_fees = universityinfo_fees
            universityinfo_vo.universityinfo_contact = universityinfo_contact
            universityinfo_vo.universityinfo_email = universityinfo_email
            universityinfo_vo.universityinfo_description = universityinfo_description
            universityinfo_dao.update_universityinfo(universityinfo_vo)
            return redirect('/admin/view_universityinfo')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_universityinfo route exception occured>>>>>>>>>>", ex)
