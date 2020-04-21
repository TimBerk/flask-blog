import os


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/flask'
    SECRET_KEY = 'kljlkfs456465sdfs4123165s4df68s432132sdf156sd4f65sdf41'

    CKEDITOR_PKG_TYPE = 'basic'

    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    SECURITY_TRACKABLE = True
    SEND_REGISTER_EMAIL = False
    SECURITY_REGISTERABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_CONFIRM_LOGIN_WITHOUT_CONFIRMATION = False
    SECURITY_POST_LOGIN_VIEW = "/"

    SECURITY_REGISTER_URL = '/register'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'photos')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
