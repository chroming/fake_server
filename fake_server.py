# -*- coding: utf-8 -*-

import click
from flask import Flask, request, send_file

app = Flask(__name__)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


@click.command()
@click.argument('text', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), required=False)
@click.option('-fc', '--file_content', type=click.Path(exists=True), required=False)
def fake_server(text, file, file_content):

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

    click.echo("Fake server started.")
    app.run()


if __name__ == '__main__':
    fake_server()