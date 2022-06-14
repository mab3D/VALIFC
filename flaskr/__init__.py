import os


from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, Response

from werkzeug.utils import secure_filename

from datetime import datetime

import json

import psycopg2


ALLOWED_EXTENSIONS = {'txt', 'ifc'}

### REPLACE !!! SET UPLOAD FOLDER, UPLOADED IFC FILES WILL BE PLACED HERE
UPLOAD_FOLDER = '\Flask\Folder'




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')

    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

# Sqlite dbase
    from . import db
    db.init_app(app)

    from . import valifc

    from . import ifcocc


### REPLACE !!! Database connection PostgreSQL
    def get_db_connection():
        conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="postgres",
                user="postgres",
                password="password")

        return conn








# Gebruik dit voor  werken db
#    with app.app_context():
#        db.get_db()

    @app.route('/info')
    def info():
        return render_template('info/info.html')

        #Sqlite
    #@app.route('/quickview')
    #def quickview():
    #    dbu = db.get_db()
    #    posts = dbu.execute(
    #        'SELECT filename, created'
    #        ' FROM ifclist'
    #        ' ORDER BY created DESC'
    #    ).fetchall()
    #    return render_template('interface/quickview.html', posts=posts)

    @app.route('/quickview')
    def quickview():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT filename, date_added FROM meta;')
        posts = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('interface/quickview.html', posts=posts)

    @app.route('/show')
    def showtest():
        m = "G:/Flask/Ondersteunend/TeUploade/IFC Schependomlaan.ifc"
        ifcocc.show(m)

#    @app.route('/')
#    def index():
#        conn = get_db_connection()
#        cur = conn.cursor()
#        cur.execute('SELECT * FROM books;')
#        books = cur.fetchall()
#        cur.close()
#        conn.close()
#        return render_template('index.html', books=books)


#### UPLOAD FUNCTIONS ####
# When a file is uploaded, this function and route is used to display it
    @app.route('/uploads/<name>')
    def download_file(name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                #return redirect(request.url)
                return render_template('interface/fail.html')
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                #return redirect(request.url)
                return render_template('interface/fail.html')
            if file and not allowed_file(file.filename):
                flash('Not a valid file extension')
                return render_template('interface/fail.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('download_file', name=filename))

            ### ValIFC code
                filefolder = UPLOAD_FOLDER
                filetype = filename[-3:]

                state = 1

                with app.app_context():
                    dbu = db.get_db()
                    dbu.execute(
                        'INSERT INTO ifclist (filename, state)'
                        ' VALUES (?, ?)',
                        (filename, state)
                    )
                    dbu.commit()
                    #return render_template('interface/succes.html')
                    jsoncontent = valifc.validate(filefolder, filename)
                    time = datetime.now()
                    time_string = time.strftime("%d%m%Y%H%M%S")
                    jsonname = str(filename)[:-4] + str(time_string)
                    jsonpath = filefolder + '/report/' + jsonname + '.json'
                    with open(jsonpath, 'w') as f:
                        json.dump(jsoncontent, f)



                    return jsoncontent
                    #return msg

                #Use this for prod
                #if filetype == 'txt':
                #    return redirect(url_for('download_file', name=filename))
                #if filetype == 'txt':
                    #ifcintake.txtcheck()

                #    return render_template('interface/succes.html')

                #else:
                #    flash('Unknown Error Route 01')
                #    return render_template('interface/fail.html')


            else:
                flash('Unknown Error Route 02')
                return render_template('interface/fail.html')


        return render_template('interface/index.html')

    return app
