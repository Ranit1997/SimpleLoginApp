# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 11:00:50 2022

@author: Ranit
"""

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, fullname, username, password):
        self.fullname = fullname
        self.username = username
        self.password = password


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        user = session['user']
        data = User.query.filter_by(username=user).first()
        details = "Username: "+data.username+"          "+"Fullname: "+data.fullname
        return render_template('home.html',message = details)
    else:
        return render_template('index.html', message="Welcome to my Login WebApp")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(fullname = request.form['fullname'],username=request.form['username'], password=request.form['password']))
            #print(request.form['fullname'])
            db.session.commit()
            return redirect(url_for('login'))
            
        except:
            #print(request.form['fullname'],request.form['username'])
            if request.form['fullname'] == "" or request.form['username'] =="" or request.form['password'] =="":
                return render_template('index.html', message="Incomplete Registration")
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            session['user']=u
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Credentials")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.secret_key = "Okok"
    db.create_all()
    app.run()