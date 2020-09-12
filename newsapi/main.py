from flask import Flask, request
from json import dumps
from modules import auth, news

app = Flask(__name__)
app.debug = True

json_header = {'Content-Type': 'application/json'}

'''
================================
         Error codes
================================

1 - Неизвестная ошибка
2 - Доступ закрыт
3 - Ошибка сервера
4 - Неверный запрос
5 - Авторизация не удалась

================================
'''


def error_json(id):
    if id == 1:
        return {
            'error_id': 1,
            'error_msg': 'Unknown error'
        }
    elif id == 2:
        return {
            'error_id': 2,
            'error_msg': 'Invalid auth token'
        }
    elif id == 3:
        return {
            'error_id': 3,
            'error_msg': 'Internal server error'
        }
    elif id == 4:
        return {
            'error_id': 4,
            'error_msg': 'Invalid request'
        }
    elif id == 5:
        return {
            'error_id': 5,
            'error_msg': 'Invalid login or password'
        }


def check_auth(req):
    token = req.cookies.get('token')
    result = auth.check_session(token)
    if result == 'error':
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(2)
            }),
            headers=json_header
        )
    else:
        return 'ok'


@app.route('/api/auth/login/', methods=['POST'])
def login():
    req = request.get_json()
    result = auth.check(login=req['login'], password=req['password'])
    if result == 'ok':
        response = app.response_class(
            response=dumps({'status': 'ok'}),
            headers=json_header,
        )
        token = auth.create_session()
        response.set_cookie('token', value=token)
        return response
    elif result == 'error':
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(3)
            }),
            headers=json_header,
        )
    else:
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(5)
            }),
            headers=json_header,
        )


@app.route('/api/auth/check/')
def check():
    token = request.cookies.get('token')
    result = auth.check_session(token)
    if result == 'ok':
        return app.response_class(
            response=dumps({'status': 'ok'}),
            headers=json_header
        )
    else:
        response = app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(2)
            }),
            headers=json_header
        )
        response.set_cookie('token', value='', expires=0)
        return response


@app.route('/api/news/get/')
def get_news():
    list_news = news.get()
    if list_news == 'error':
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(3)
            }),
            headers=json_header
        )
    else:
        id = request.args.get('id')
        if id is None:
            return app.response_class(
                response=dumps({
                    'status': 'ok',
                    'response': list_news
                }),
                headers=json_header
            )
        else:
            result = news.get_by_id(id)
            if result is None:
                return app.response_class(
                    response=dumps({
                        'status': 'ok',
                        'response': []
                    }),
                    headers=json_header
                )
            elif result == 'error':
                return app.response_class(
                    response=dumps({
                        'status': 'error',
                        'error': error_json(3)
                    }),
                    headers=json_header
                )
            else:
                return app.response_class(
                    response=dumps({
                        'status': 'ok',
                        'response': result
                    }),
                    headers=json_header
                )


@app.route('/api/news/remove/')
def remove_news():
    check_result = check_auth(request)
    if check_result != 'ok':
        return check_result

    id = request.args.get('id')
    if id is None:
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(4)
            }),
            headers=json_header
        )
    else:
        result = news.remove(id)
        if result == 'ok':
            return app.response_class(
                response=dumps({'status': 'ok'}),
                headers=json_header
            )
        else:
            return app.response_class(
                response=dumps({
                    'status': 'error',
                    'error': error_json(3)
                }),
                headers=json_header
            )


@app.route('/api/news/add/', methods=['POST'])
def add_news():
    check_result = check_auth(request)
    if check_result != 'ok':
        return check_result

    json = request.get_json()
    if json['title'] == '' or json['preview'] == '' or json['body'] == '':
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(4)
            }),
            headers=json_header
        )
    result = news.add(title=json['title'], preview=json['preview'], body=json['body'])
    if result == 'ok':
        return app.response_class(
            response=dumps({'status': 'ok'}),
            headers=json_header
        )
    else:
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(3)
            }),
            headers=json_header
        )


@app.route('/api/news/edit/', methods=['POST'])
def edit_news():
    check_result = check_auth(request)
    if check_result != 'ok':
        return check_result

    json = request.get_json()
    if json['id'] == '' or json['title'] == '' or json['preview'] == '' or json['body'] == '':
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(4)
            }),
            headers=json_header
        )
    result = news.edit(id=json['id'], title=json['title'], preview=json['preview'], body=json['body'])
    if result == 'ok':
        return app.response_class(
            response=dumps({'status': 'ok'}),
            headers=json_header
        )
    else:
        return app.response_class(
            response=dumps({
                'status': 'error',
                'error': error_json(3)
            }),
            headers=json_header
        )


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
