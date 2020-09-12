import pymysql
import yaml

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


def get():
    try:
        n = req('SELECT * FROM articles')
    except:
        return 'error'
    else:
        if n == ():
            return []
        else:
            return n


def get_by_id(id):
    try:
        n = req('SELECT * FROM articles WHERE id=%s', id)
    except:
        return 'error'
    else:
        if n == ():
            return None
        else:
            return n[0]


def remove(id):
    try:
        req('DELETE FROM articles WHERE id=%s', id)
    except:
        return 'error'
    else:
        return 'ok'


def add(title, preview, body):
    try:
        req('INSERT INTO articles (title, preview, body) VALUES (%s, %s, %s)', (title, preview, body))
    except:
        return 'error'
    else:
        return 'ok'


def edit(id, title, preview, body):
    try:
        req('UPDATE articles SET title=%s, preview=%s, body=%s WHERE id=%s', (title, preview, body, id))
    except:
        return 'error'
    else:
        return 'ok'
