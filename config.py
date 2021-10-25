import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('asdaldfi2ifjadfi9u8') or 'a1d2f3g4'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA3_PUBLIC_KEY = "6LeuMsMcAAAAAJ4BIp_YEr254_bljnCTH9SWrOY4"
    RECAPTCHA3_PRIVATE_KEY = "6LeuMsMcAAAAAHLg4ZHovJMJBidpo_LwcCZGSq6K"
    POSTS_PER_PAGE = 15
    COMMENTS_PER_PAGE = 10
    ACCOUNTS_PER_PAGE = 15
