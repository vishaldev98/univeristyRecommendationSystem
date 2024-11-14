from flask import render_template

from base import app

DATASET_FOLDER = 'base/static/adminResources/dataset/'

app.config['DATASET_FOLDER'] = DATASET_FOLDER


#
# @app.route('/')
# def hello_world():
#     return render_template('admin/index.html')


@app.route('/admin/view_user')
def admin_view_user():
    return render_template('admin/manageUser.html')


@app.route('/admin/reply_complain')
def reply_complain():
    return render_template('admin/replyComplain.html')


@app.route('/user/request_prediction')
def user_request_prediction():
    return render_template('user/addPrediction.html')
