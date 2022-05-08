import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess-this-secret-key'
SEND_FILE_MAX_AGE_DEFAULT = -1

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

USER_EMAIL_SENDER_EMAIL = "example@email.com"

ALLOWED_EXTENSIONS = {'pdf'}

UPLOAD_FOLDER = os.path.abspath(".") + "\\app\\static\\textbooks\\"
