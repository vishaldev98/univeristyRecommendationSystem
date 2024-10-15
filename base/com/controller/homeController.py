from flask import render_template

from base import app


@app.route('/admin/view_user')
def viewUser():
    try:
        return render_template('admin/viewUser.html')
    except Exception as ex:
        print("admin_view_user route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/view_details')
def viewDetails():
    try:
        return render_template('admin/viewDetails.html')
    except Exception as ex:
        print("admin_view_details route exception occurred>>>>>>>>>>", ex)


@app.route('/admin/view_prediction')
def viewPrediction():
    try:
        return render_template('admin/viewPrediction.html')
    except Exception as ex:
        print("admin_view_prediction route exception occurred>>>>>>>>>>", ex)
