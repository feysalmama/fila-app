from flask import Flask,render_template,redirect,request,url_for,escape, session ,flash,send_from_directory
import pymysql
import os
from flask_wtf import Form
from wtforms import StringField , TextField,TextAreaField,RadioField
from wtforms.validators import DataRequired
from werkzeug.utils import  secure_filename
app = Flask(__name__)
db =pymysql.connect(host="localhost",user="root",passwd="amlaml",db="flask")
cur = db.cursor()
# folder to be kept the uploaded file
UPLOADED_DIR = 'E:/uploads/'
app.config['UPLOAD_FOLDER']=UPLOADED_DIR
# files allowed to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['doc','png','jpg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('hello_world',name=session['username']))
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        cur.execute("SELECT COUNT(1) FROM user WHERE name=%s;",[user_name])
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE name=%s;",[user_name])
            for row in cur.fetchall():
                if password == row[0]:
                    session['username']=request.form['username']
                    flash('you ware successfully loged in ','info')
                    return redirect(url_for('hello_world',name=user_name))
                else:
                    error = "invalid credential here"

        else:
            error = "invalid credential"
    call = "Well Come to ToLearn"
    return render_template('login.html',error=error ,well=call)

@app.route('/registration',methods=['GET','POST'])
def registration():
    error = None
    if request.method == 'POST':
        user_name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        cur.execute("INSERT INTO user (name,email,password) VALUES (%s,%s,%s)",(user_name,email,password))
        db.commit()
        error = "Successfully Register"
    return render_template('registration.html' ,error = error)

@app.route('/index/<name>')
def hello_world(name):
    if 'username' in session:
        user_session = escape(session['username'])
        return render_template('index.html',name=user_session)
    else:
        return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('base.html')
@app.route('/signUp')
def signUp():
    goodby = session['username']
    session.pop('username',None)
    return redirect(url_for('login',goodbya='Good by '+goodby))

@app.route('/upload' , methods=['GET','POST'])
def upload():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            error='No file selected'
        else:
            if not os.path.isdir(UPLOADED_DIR):
                 os.makedirs(UPLOADED_DIR)
                 if file and allowed_file(file.filename):
                     filename = secure_filename(file.filename)
                     file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                 else:
                     error = "file you try to upload is not allowed"
    return render_template('upload.html', error=error)

@app.route('/productList')
def productList():

    if 'username' in session:
        cur.execute("SELECT * FROM product ")
        rows = cur.fetchall()
    else:
        return redirect(url_for('login'))

    return render_template('product.html' ,rows = rows)

app.secret_key = 'theworldthiredwarcameaftersomething'
if __name__ == '__main__':
    app.run(debug=True)
