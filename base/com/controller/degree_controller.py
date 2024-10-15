from flask import request, render_template, redirect

from base import app
from base.com.dao.degree_dao import DegreeDAO
from base.com.vo.degree_vo import DegreeVO


@app.route('/admin/load_degree', methods=['GET'])
def admin_load_degree():
    try:
        return render_template('admin/addDegree.html')
    except Exception as ex:
        print("admin_load_degree route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/insert_degree', methods=['POST'])
def admin_insert_degree():
    try:
        degree_name = request.form.get('degreeName')
        degreeDescription = request.form.get('degreeDescription')

        degree_vo = DegreeVO()
        degree_dao = DegreeDAO()

        degree_vo.degree_name = degree_name
        degree_vo.degree_description = degreeDescription
        degree_dao.insert_degree(degree_vo)
        return redirect('/admin/view_degree')
    except Exception as ex:
        print("admin_insert_degree route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/view_degree', methods=['GET'])
def admin_view_degree():
    try:
        degree_dao = DegreeDAO()
        degree_vo_list = degree_dao.view_degree()
        return render_template('admin/viewDegree.html', degree_vo_list=degree_vo_list)
    except Exception as ex:
        print("admin_view_degree route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/delete_degree', methods=['GET'])
def admin_delete_degree():
    try:
        degree_vo = DegreeVO()
        degree_dao = DegreeDAO()

        degree_id = request.args.get('degreeId')
        print("In delete degree>>>>>>>>>>>>>>", degree_id)
        degree_vo.degree_id = degree_id
        degree_dao.delete_degree(degree_vo)
        return redirect('/admin/view_degree')
    except Exception as ex:
        print("admin_delete_degree route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/edit_degree', methods=['GET'])
def admin_edit_degree():
    try:
        degree_vo = DegreeVO()
        degree_dao = DegreeDAO()

        degree_id = request.args.get('degreeId')
        degree_vo.degree_id = degree_id
        degree_vo_list = degree_dao.edit_degree(degree_vo)
        print("in admin_edit_degree degree_vo_list>>>>>>", degree_vo_list)
        print("in admin_edit_degree type of degree_vo_list>>>>>>>", type(degree_vo_list))
        return render_template('admin/editDegree.html', degree_vo_list=degree_vo_list)
    except Exception as ex:
        print("admin_edit_degree route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/update_degree', methods=['POST'])
def admin_update_degree():
    try:
        degree_id = request.form.get('degreeId')
        degree_name = request.form.get('degreeName')
        degree_description = request.form.get('degreeDescription')

        degree_vo = DegreeVO()
        degree_dao = DegreeDAO()

        degree_vo.degree_id = degree_id
        degree_vo.degree_name = degree_name
        degree_vo.degree_description = degree_description
        degree_dao.update_degree(degree_vo)
        return redirect('/admin/view_degree')
    except Exception as ex:
        print("admin_update_degree route exception occurred>>>>>>>>>>", ex)
