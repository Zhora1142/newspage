import hashlib
import pymysql
import yaml
import random
import string
from os import listdir

sql = yaml.load(open('config.yml').read())['mysql']


def req(*args):
    db = pymysql.connect(host=sql['host'], user=sql['username'], passwd=sql['password'], db=sql['database'],
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    crs = db.cursor()
    crs.execute(*args)
    result = crs.fetchall()
    db.commit()
    db.close()
    return result


def generate_token():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(32)))
    return result_str


def check(login, password):
    try:
        base = req('SELECT * FROM admins WHERE login=%s', login)
    except:
        return 'error'
    else:
        if base != ():
            base = base[0]
            password = hashlib.md5(password.encode()).hexdigest()
            if password == base['password']:
                return 'ok'
            else:
                return 'wrong_password'
        else:
            return 'wrong_login'


def create_session():
    token = generate_token()
    file = open('tokens/' + token, 'w')
    file.close()
    return token


def check_session(token):
    if token in listdir('tokens'):
        return 'ok'
    else:
        return 'error'
