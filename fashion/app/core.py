# -*- coding: utf-8 -*-

server = None

def Init():
	from flask import Flask
	app = Flask(__name__)
	#import os
	#app.config.from_object('app.config.DefaultConfig')
	app.secret_key = 'e8742af3954a284f398f1699989cf7effa2960b2bf1fe92e'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mydb:mydb@127.0.0.1/userinfo'
	app.config['BCRYPT_LEVEL'] = 63
	app.config['static_url_path'] = '/home/fashion/app/static'
	
	from flask.ext.sqlalchemy import SQLAlchemy
	db = SQLAlchemy(app)

	class MakeServerObject(object): pass
	global server
	server = MakeServerObject()
	server.app = app
	server.db = db
	#server.config = app.config
	return server
