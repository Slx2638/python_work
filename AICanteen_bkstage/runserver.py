from demo import app

from flask import render_template




if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=11453)
    #app.run(debug=True,host='0.0.0.0',port=11453,ssl_context='adhoc')

    app.run(debug=True,port=5000)
