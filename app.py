from flask import Flask, render_template, request, flash, redirect, url_for, session
import os

from flask_pymongo import PyMongo

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'kanban'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/kanban'


mongo = PyMongo(app)

@app.route('/')
def index():
    users = mongo.db.users
    alluser = users.find()

    return render_template('index.html')

@app.route('/<fname>')
def display_name(fname):

    return render_template('index.html',fname=fname)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        users = mongo.db.users
        founduser = users.find_one({'email':email, 'password':password})
        if founduser is None:
            error = "password not matched"
            flash('Incorrect password','danger')
            return render_template("login.html")            
        else:
            session['name']=founduser['name']
            session['email']=founduser['email']
            session['logged_in']=True
            flash('Login Successfull','success')
            return redirect(url_for('index'))

    return render_template("login.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form['fname'] +" "+ request.form['lname']
        email = request.form['email']
        password = request.form['password']
        users = mongo.db.users
        datainserted = users.insert({'name':name, 'email':email,'password':password})
        if datainserted:
            flash('Successfully registered','success')
            session['name']=name
            session['email']=email
            session['logged_in']=True
            return redirect(url_for('index'))
        else:
            flash('Duh Duh Duh!!! Something went wrong. Try Again')
            return redirect(url_for('signup'))


       
            
            
    return render_template("signup.html")



@app.route('/board',methods=['POST','GET'])
def board():
    return render_template("board.html")

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.clear()
        flash('Successfully logged out','success')
        return redirect(url_for('login'))
    else:
        flash('You are not Logged in','secondary')
        return redirect(url_for('login'))

@app.route('/upload',methods=['POST','GET'])
def upload():
    users = mongo.db.users
    path = os.path.abspath('static/img')
    app.config['UPLOAD_FOLDER'] = path

    if request.method == 'POST':
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(f)

        users.update({'email':session['email']},{'$set':{'image':'img/'+file.filename}})
        flash('Successfully upload','success')

    user = users.find_one({'email':session['email']})

    return render_template("image_upload.html")

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug='true',port='8080')
