# -*- coding: utf-8 -*-

import multiprocessing
import platform

import click
from flask import Flask, request, send_file
import gunicorn.app.base

app = Flask(__name__)

VERSION = '0.2'


def get_system():
    pf = platform.platform()
    if pf.startswith('Darwin'):
        return 'macOS'
    else:
        return 'Other'


system = get_system()


HTTP_METHODS = {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'}
DEFAULT_HOST = '0.0.0.0' if system == 'macOS' else '127.0.0.1'
DEFAULT_PORT = 8000
DEFAULT_SERVER_KEY = 'local_server.key'
DEFAULT_SERVER_CRT = 'local_server.crt'


number_of_workers = (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, ap, options=None):
        self.options = options or {}
        self.application = ap
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, https=True, server_key=DEFAULT_SERVER_KEY, server_crt=DEFAULT_SERVER_CRT):
    options = {
        'bind': '%s:%s' % (host, port),
        'workers': number_of_workers,
    }
    if https:
        options.update({
            'certfile': server_crt,
            'keyfile': server_key
    })
    StandaloneApplication(app, options).run()


@click.command()
@click.option('-t', '--text', type=click.STRING, required=False,
              help='Return text, default "Success"')
@click.option('-f', '--file', type=click.Path(exists=True), required=False,
              help='Return file as attachment')
@click.option('-fc', '--file_content', type=click.Path(exists=True), required=False,
              help='Return file content')
@click.option('-b', '--bind', type=click.STRING, required=False,
              help='''Server bind host and port, default 127.0.0.1:80, 
                   if you what listen on all interface just use 0.0.0.0:80''')
@click.option('-p', '--port', type=click.INT, required=False,
              help='Server bind port, same as port in --bind, default 80')
@click.option('-s', '--https', is_flag=True, required=False, help='Use https or not')
@click.option('-sk', '--server_key', type=click.STRING, required=False,
              help='Server key file path, default ./local_server.key')
@click.option('-sc', '--server_crt', type=click.STRING, required=False,
              help='Server cert file path, default ./local_server.key')
@click.version_option(VERSION, '-v', '--version')
@click.help_option('-h', '--help')
def fake_server(text, file, file_content, bind, port, server_key, server_crt, https=True):
    if bind and ':' in bind:
        host, port = bind.split(':')
    else:
        host = bind
        port = port
    host = host or DEFAULT_HOST
    port = port or DEFAULT_PORT
    methods = HTTP_METHODS

    @app.route('/', defaults={'path': ''}, methods=methods)
    @app.route('/<path:path>', methods=methods)
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
    run_server(host, port, https, server_key, server_crt)


if __name__ == '__main__':
    fake_server()