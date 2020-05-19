# -*- coding: utf-8 -*-


from flask import Flask, request
app = Flask(__name__)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/<path:path>')
def catch_all(path):
    print("Try to {method} path {path}".format(method=request.method, path=request.path))
    return "success"


if __name__ == '__main__':
    app.run()