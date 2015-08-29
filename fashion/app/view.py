# -*- coding: utf-8 -*-

from functools import wraps
from core import server
from flask import session, render_template, request, redirect, url_for, jsonify
from model import *
from datetime import timedelta
from flask.ext.bcrypt import Bcrypt
from werkzeug import secure_filename
import os
import string

app = server.app
bcrypt = Bcrypt(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def login_required(f):
	@wraps(f)
	def deco(*args, **kwargs) :
		if 'userid' in session :
			return f(*args, **kwargs)
		print 'not in session'
		return redirect(url_for('login_page'))
	return deco

@app.before_request
def session_reset():
	session.modified = True
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/',methods = ['GET'])
def main_page():
	userid = None
	if 'userid' in session :
		userid = session['userid']
	if 'page' in session :
		session['page'] = 0
	images = Document.query.limit(8).all();
	return render_template('index.html', images = images, userid = userid)
@app.route('/getimages', methods= ['GET'])
def get_image():
	if not 'page' in session :
		session['page'] = 1
		page = 1
	else :
		page = session['page']
		page = page + 1
		session['page'] = page

	temp = 4 + 4*page
	images = {}
	for i in range(1,5) :
		aimage = Document.query.get(temp+i);
		if aimage is not None :
			images.update({i:aimage.path})
		aimage = None
	return jsonify(images)

@app.route('/login/post', methods = ['POST'])
def login_post():
	userid = request.form.get('userid','')
	password = request.form.get('password','')
	
	loginuser = User.query.filter_by(userid = userid).first()
	if loginuser is None or not bcrypt.check_password_hash(loginuser.passwd, password):
		print 'Userid or Password is invalid'
	elif 'userid' in session :
		print 'already logined'
	else : 
		session['userid'] = userid;
		print 'login successfully'
	return redirect(url_for('main_page'))	
	
@app.route('/logout')
def logout():
	session.pop('userid', None)
	return redirect(url_for('main_page'))

@app.route('/register', methods = ['GET'])
def register_page():

	userid = None
	if 'userid' in session :
		userid = session['userid']
	return render_template('register.html', userid = userid)
		

def check_user_info(userid, password) :
	sameuser = User.query.filter_by(userid = userid).first()
	if '' in [userid, password] or sameuser is not None :
		return False
	if len(unicode(password)) <=5 or len(unicode(userid)) <=5 or\
		len(unicode(password)) >=12 or len(unicode(userid)) >=12 :
		return False 
	if len(set(string.punctuation).intersection(password)) > 0 or \
		len(set(string.punctuation).intersection(userid)) > 0 :
		return False
	return True
@app.route('/register/post', methods = ['POST'])
def register_post():
	userid = request.form.get('userid','')
	password = request.form.get('password','')
	if not check_user_info(userid, password) :
		return redirect(url_for('register_page'))
		
	user = User(userid, bcrypt.generate_password_hash(password))
	try :
		db.session.add(user)
		db.session.commit()
	except Exception:
		db.session.rollback()
		return redirect(url_for('register_page'));
		
	return redirect(url_for('main_page'))
	
@app.route('/uploadpage', methods = ['GET'])
@login_required
def upload_page():

	userid = None
	if 'userid' in session :
		userid = session['userid']
	return render_template('uploadpage.html', userid = userid)

def root_dir():
	return os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadpage/post', methods=['POST'])
@login_required
def upload_post():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename) 
		path = '/static/images/' + session['userid'] + '/'
		
		if not os.path.exists(root_dir() + path) :
			os.makedirs(root_dir() + path)
			
		file.save(os.path.join(root_dir() + path, filename))

		content = request.form.get('content','')
		bodytype = request.form.get('r',0)
		user = User.query.filter_by(userid = session['userid']).first()
		document = Document(path = 'images/'+session['userid'] + '/' + filename, content = content, bodytype = bodytype, good = 0)
		board = Board()
		board.document.append(document)
		board.user = user
		try :
			db.session.add(document)
			db.session.add(board)
			db.session.commit()
		except Exception:
			db.session.rollback()

		return redirect(url_for('main_page'))
	return redirect(url_for('upload_page'))

@app.route('/mypage',methods=['GET'])
@login_required
def mypage():

	userid = None
	if 'userid' in session :
		userid = session['userid']
	return render_template('mypage.html', userid = userid)


