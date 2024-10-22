from flask import render_template

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.user_dao import UserDAO

@app.route('/admin/view_user')
def viewUser():
    try:
        if admin_login_session() == "admin":
            user_dao = UserDAO()  # Create an instance of UserDAO
            users = user_dao.get_all_users()  # Fetch all users
            return render_template('admin/viewUser.html', users=users)  # Pass the users to the template
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_user route exception occurred:", ex)
        return "An error occurred while fetching user data."


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