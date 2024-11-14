from flask import request, render_template, redirect, url_for

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.degree_dao import DegreeDAO
from base.com.dao.department_dao import DepartmentDAO
from base.com.vo.department_vo import DepartmentVO


@app.route('/admin/load_department')
def admin_load_department():
    try:
        if admin_login_session() == "admin":
            degree_dao = DegreeDAO()
            degree_vo_list = degree_dao.view_degree()
            return render_template('admin/addDepartment.html', degree_vo_list=degree_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_load_department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_department', methods=['POST'])
def admin_insert_department():
    try:
        if admin_login_session() == "admin":
            department_name = request.form.get('departmentName')
            department_description = request.form.get('departmentDescription')
            department_degree_id = request.form.get('departmentDegreeId')

            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_vo.department_name = department_name
            department_vo.department_description = department_description
            department_vo.department_degree_id = department_degree_id
            department_dao.insert_department(department_vo)
            return redirect(url_for('admin_view_department'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_insert_department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_department')
def admin_view_department():
    try:
        if admin_login_session() == "admin":
            department_dao = DepartmentDAO()
            department_vo_list = department_dao.view_department()
            print("department_vo_list>>>>>>>>>>", department_vo_list)
            return render_template('admin/viewDepartment.html', department_vo_list=department_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_view_department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_department', methods=['GET'])
def admin_delete_department():
    try:
        if admin_login_session() == "admin":
            department_dao = DepartmentDAO()
            department_id = request.args.get('departmentId')
            department_dao.delete_department(department_id)
            return redirect(url_for('admin_view_department'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_delete_department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/edit_department', methods=['GET'])
def admin_edit_department():
    try:
        if admin_login_session() == "admin":
            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()
            degree_dao = DegreeDAO()

            department_id = request.args.get('departmentId')
            department_vo.department_id = department_id
            department_vo_list = department_dao.edit_department(department_vo)
            degree_vo_list = degree_dao.view_degree()
            return render_template('admin/editDepartment.html', degree_vo_list=degree_vo_list,
                                   department_vo_list=department_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_edit_department route exception occured>>>>>>>>>>", ex)


@app.route('/admin/update_department', methods=['POST'])
def admin_update_department():
    try:
        if admin_login_session() == "admin":
            department_id = request.form.get('departmentId')
            department_name = request.form.get('departmentName')
            department_description = request.form.get('departmentDescription')
            department_degree_id = request.form.get('departmentDegreeId')

            department_vo = DepartmentVO()
            department_dao = DepartmentDAO()

            department_vo.department_id = department_id
            department_vo.department_name = department_name
            department_vo.department_description = department_description
            department_vo.department_degree_id = department_degree_id
            department_dao.update_department(department_vo)
            return redirect(url_for('admin_view_department'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_update_department route exception occured>>>>>>>>>>", ex)
