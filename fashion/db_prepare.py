# -*- coding:utf-8 -*-

import app.core

server = app.core.Init()
db = server.db

from model import *
db.drop_all()
db.create_all()

