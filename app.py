from base import app


if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='localhost', port=2807)
