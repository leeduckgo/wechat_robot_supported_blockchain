# -*- coding: utf-8 -*-
import os
CSRF_ENABLED = True
SECRET_KEY = '123456'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'gv_files.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
