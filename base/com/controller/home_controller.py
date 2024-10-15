from flask import render_template

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session


@app.route('/admin/view_user')
def viewUser():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/viewUser.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_details')
def viewDetails():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/viewDetails.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_details route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_prediction')
def viewPrediction():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/viewPrediction.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_prediction route exception occured>>>>>>>>>>", ex)


