from flask import Flask, render_template, redirect, request, url_for, escape, session, flash, send_file, abort
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
db = pymysql.connect(host="localhost", user="root", passwd="amlaml", db="flask")
cur = db.cursor()
# folder to be kept the uploaded file
UPLOADED_DIR = 'E:/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOADED_DIR
# files allowed to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'docx', 'png', 'jpg', 'gif', 'mp4', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('hello_world', name=session['username']))
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        if user_name != '' and email != '' and password != '':
            cur.execute("SELECT COUNT(1) FROM user WHERE u_name=%s;", [user_name])
            if cur.fetchone()[0]:
                cur.execute("SELECT password FROM user WHERE u_name=%s;", [user_name])
                for row in cur.fetchall():
                    if password == row[0]:
                        session['username'] = request.form['username']
                        flash('you ware successfully logged in ', 'info')
                        return redirect(url_for('hello_world', name=user_name))
                    else:
                        error = "credential is not match"
            else:
                error = "no valid credential data"
        else:
            error = "please fill all filled"

    call = "Well Come to ToLearn"
    return render_template('login.html', error=error, well=call)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    error = None
    message = None
    if request.method == 'POST':

        full_name = request.form['f_name']
        user_name = request.form['u_name']
        collage = request.form['collage']
        faculty = request.form['faculty']
        department = request.form['department']
        email = request.form['email']
        password = request.form['pass']
        if full_name!=''and collage !=''and faculty!='' and department!='' and  user_name != '' and  email != '' and  password != '':
            cur.execute("INSERT INTO user (full_name ,u_name,collage,faculty,Department,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s)", ( full_name,user_name,collage,faculty,department , email, password))
            db.commit()
            message = "Successfully Register"
        else:
            error = "all fields must be filled"
    return render_template('registration.html', error=error, message=message)


# @app.route('/', defaults={'name': None})
# @app.route('/index', defaults={'name': 'Saba koo'})
@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/logout')
def logout():
    goodby = None
    if 'username' in session:
        goodby = session['username']
        session.pop('username', None)
    else:
        return render_template('login.html')
    return redirect(url_for('login', goodbya='Good by ' + goodby))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    error = None
    message = None
    if 'username' in session:
        if request.method == 'POST':
            file = request.files['file']
            if file.filename == '':
                error = 'No file selected'
            else:
                if file and allowed_file(file.filename):
                    if not os.path.isdir(UPLOADED_DIR):
                        os.makedirs(UPLOADED_DIR, mode=0o777)
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        message = "file uploaded successfully"
                    else:
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        message = "file uploaded successfully"
                else:
                    error = "file you try to upload is not allowed"
    else:
        return redirect(url_for('login'))
    return render_template('upload.html', error=error, message=message)


@app.route('/productList')
def productList():
    if 'username' in session:
        cur.execute("SELECT * FROM user ")
        rows = cur.fetchall()
    else:
        return redirect(url_for('login'))

    return render_template('product.html', rows=rows)


@app.route('/saved_file')
def saved_file():
    toggle = 0
    if not os.path.exists(UPLOADED_DIR):
        return abort(404)
    if os.path.isfile(UPLOADED_DIR):
        return send_file(UPLOADED_DIR)
    files = os.listdir(UPLOADED_DIR)
    return render_template('browseFile.html', files=files, toggle=toggle ,fileLocation=UPLOADED_DIR)


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/login')
def login_agian():
    if 'username' in session:
        return redirect(url_for('hello_world', name=session['username']))
    return render_template('login.html')


@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/about')
def about():
    return render_template('about.html')


app.secret_key = 'teleconferencing'
if __name__ == '__main__':
    app.run(debug=True)
