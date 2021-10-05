import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 15
    RECAPTCHA_USE_SLL = False
    RECAPTCHA_PUBLIC_KEY = "6LdoUK4cAAAAAL5mcru6hcfpKmP8CBugJS8M-uEx"
    RECAPTCHA_PRIVATE_KEY = "6LdoUK4cAAAAAArrnU_-Ggdm2E4LdU4AoSUd1j5q"
    RECAPTCHA_OPTIONS = {'theme': 'black'}
