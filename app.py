from base import app

port_number = 5671

if __name__ == "__main__":
    app.run(threaded=True, host='localhost', port=port_number)


# python flask orm libs
# pip install flask
# pip install pymysql
# pip install sqlalchemy
# pip install flask-sqlalchemy