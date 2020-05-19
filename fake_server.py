# -*- coding: utf-8 -*-

import multiprocessing

import click
from flask import Flask, request, send_file
import gunicorn.app.base

app = Flask(__name__)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = '80'


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run_server(host='127.0.0.1', port=80):
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': number_of_workers(),
    }
    StandaloneApplication(app, options).run()


@click.command()
@click.argument('text', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), required=False)
@click.option('-fc', '--file_content', type=click.Path(exists=True), required=False)
@click.option('-b', '--bind', type=click.STRING, required=False)
def fake_server(text, file, file_content, bind):
    if bind and ':' in bind:
        host, port = bind.split(':')
    else:
        host = bind
        port = DEFAULT_PORT
    host = host or DEFAULT_HOST
    port = port or DEFAULT_PORT

    @app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
    @app.route('/<path:path>')
    def catch_all(path):
        print("Try to {method} path {path}".format(method=request.method, path=request.path))
        if text:
            return text
        elif file:
            return send_file(file, as_attachment=True)
        elif file_content:
            return send_file(file_content)
        else:
            return 'Success'

    click.echo("Fake server started at: {host}:{port}".format(host=host, port=port))
    run_server(host, port)


if __name__ == '__main__':
    fake_server()