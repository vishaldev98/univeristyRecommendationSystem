import os
from datetime import datetime

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.dataset_dao import DatasetDAO
from base.com.vo.dataset_vo import DatasetVO

DATASET_FOLDER = 'base/static/adminResources/dataset/'

app.config['DATASET_FOLDER'] = DATASET_FOLDER


@app.route('/admin/load_dataset')
def admin_load_dataset():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/addDataset.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_dataset route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_dataset', methods=['POST'])
def admin_insert_dataset():
    try:
        if admin_login_session() == "admin":
            dataset_file = request.files.get('datasetFile')
            dataset_description = request.form.get('datasetDescription')

            dataset_file_name = secure_filename(dataset_file.filename)
            dataset_file_path = os.path.join(app.config['DATASET_FOLDER'])
            dataset_file.save(os.path.join(dataset_file_path, dataset_file_name))
            dataset_datetime = datetime.now()

            dataset_vo = DatasetVO()
            dataset_dao = DatasetDAO()

            dataset_vo.dataset_datetime = dataset_datetime
            dataset_vo.dataset_file_name = dataset_file_name
            dataset_vo.dataset_file_path = dataset_file_path.replace("base", "..")
            dataset_vo.dataset_description = dataset_description
            dataset_dao.insert_dataset(dataset_vo)

            return redirect(url_for('admin_view_dataset'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_dataset route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_dataset')
def admin_view_dataset():
    try:
        if admin_login_session() == "admin":
            dataset_dao = DatasetDAO()
            dataset_vo_list = dataset_dao.view_dataset()
            return render_template('admin/viewDataset.html', dataset_vo_list=dataset_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_dataset route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_dataset', methods=['GET'])
def admin_delete_dataset():
    try:
        if admin_login_session() == "admin":
            dataset_dao = DatasetDAO()
            dataset_id = request.args.get('datasetId')
            print(dataset_id)
            dataset_vo_list = dataset_dao.delete_dataset(dataset_id)
            file_path = dataset_vo_list.dataset_file_path.replace("..", "base") + dataset_vo_list.dataset_file_name
            os.remove(file_path)
            return redirect(url_for('admin_view_dataset'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_dataset route exception occured>>>>>>>>>>", ex)
