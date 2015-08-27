from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.core import server
from datetime import datetime
db = server.db

class User(db.Model) :
	__tablename__='user'
	id = db.Column(db.Integer, primary_key = True)
	userid = db.Column(db.String(128), unique = True)
	username = db.Column(db.String(128))
	passwd = db.Column(db.String(128))

	boardid = db.Column(db.Integer, ForeignKey('board.id'))
	commentid = db.Column(db.Integer, ForeignKey('comment.id'))

	def __init__ (self, userid, passwd) :
		self.userid = userid
		self.passwd = passwd	


class Board(db.Model) :
	__tablename__='board'
	id = db.Column(db.Integer, primary_key = True)
	user = db.relationship('User', backref = 'Board', uselist = False)
	document = db.relationship('Document', order_by='desc(Document.time)', backref = 'Board')

class Document(db.Model) :
	__tablename__='document'

	id = db.Column(db.Integer, primary_key = True)

	path = db.Column(db.String(512))
	content = db.Column(db.String(4096))
	time = db.Column(db.DateTime, nullable=False)
	bodytype = db.Column(db.Integer)
	good = db.Column(db.Integer, default = 0)

	boardid = db.Column(db.Integer, ForeignKey('board.id'))

	comment = db.relationship('Comment', order_by = 'desc(Document.time)')

	def __init__ (self, path, content, bodytype, good) :
		self.path = path
		self.content = content
		self.bodytype = bodytype
		self.good = good
		self.time = datetime.now()
		
class Comment(db.Model):
	__tablename__ = 'comment'
	
	id = db.Column(db.Integer, primary_key = True)

	time = db.Column(db.DateTime, nullable=False)
	comment = db.Column(db.String(256))
	
	documentid = db.Column(db.Integer, ForeignKey('document.id'))
	user = db.relationship('User', uselist = False)


	def __init__(self, userid, username, boardid, comment) :
		self.userid = userid
		self.username = username
		self.boardid = board.id
		self.time = datetime.now()
		self.comment = comment
	
		
	