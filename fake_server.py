# -*- coding: utf-8 -*-

import sys
import asyncio
import platform
import multiprocessing


import click
from loguru import logger
from quart import Quart, request, send_file
from hypercorn.config import Config
from hypercorn.asyncio import serve


app = Quart(__name__)

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
DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
DEFAULT_SERVER_KEY = 'local_server.key'
DEFAULT_SERVER_CRT = 'local_server.crt'


number_of_workers = (multiprocessing.cpu_count() * 2) + 1


def run_server(host=DEFAULT_HOST, port=DEFAULT_HTTP_PORT, https=True, server_key=DEFAULT_SERVER_KEY, server_crt=DEFAULT_SERVER_CRT):
    config = Config()
    config.bind = ["%s:%s" % (host, port)]
    asyncio.run(serve(app, config))


@click.command()
@click.option('-t', '--text', type=click.STRING, required=False,
              help='Return text, default "Success"')
@click.option('-f', '--file', type=click.Path(exists=True), required=False,
              help='Return file as attachment')
@click.option('-fc', '--file_content', type=click.Path(exists=True), required=False,
              help='Return file content')
@click.option('-b', '--bind', type=click.STRING, required=False,
              help='''Server bind host and port, default {host}:{http_port} or {host}:{https_port}(for https), 
                   if you what listen on all interface just use 0.0.0.0:80'''.format(
                  host=DEFAULT_HOST, http_port=DEFAULT_HTTP_PORT, https_port=DEFAULT_HTTPS_PORT))
@click.option('-p', '--port', type=click.INT, required=False,
              help='Server bind port, same as port in --bind, default %s or %s(for https)'
                   % (DEFAULT_HTTP_PORT, DEFAULT_HTTPS_PORT))
@click.option('-s', '--https', is_flag=True, required=False, help='Use https or not')
@click.option('-sk', '--server_key', type=click.STRING, required=False,
              help='Server key file path, default ./local_server.key')
@click.option('-sc', '--server_crt', type=click.STRING, required=False,
              help='Server cert file path, default ./local_server.key')
@click.option('--debug', is_flag=True, required=False, help='Output all request data for debug')
@click.version_option(VERSION, '-v', '--version')
@click.help_option('-h', '--help')
def fake_server(text, file, file_content, bind, port, server_key, server_crt, https=True, debug=False):
    if bind and ':' in bind:
        host, port = bind.split(':')
    else:
        host = bind
        port = port
    host = host or DEFAULT_HOST
    port = port or (DEFAULT_HTTPS_PORT if https else DEFAULT_HTTP_PORT)
    methods = HTTP_METHODS

    @app.route('/', defaults={'path': ''}, methods=methods)
    @app.route('/<path:path>', methods=methods)
    async def catch_all(path):
        logger.remove()
        logger.add(sys.stderr, level="DEBUG" if debug else "INFO")
        logger.info("Try to {method} path {path}".format(method=request.method, path=request.path))
        logger.debug("Full path: {full_path}".format(full_path=request.full_path))
        logger.debug("Header: \n{header}".format(header=request.headers))
        logger.debug("Data: \n{data}".format(data=await request.data))

        if text:
            return text
        elif file:
            return await send_file(file, as_attachment=True)
        elif file_content:
            return await send_file(file_content)
        else:
            return 'Success'

    click.echo("Fake server started at: {host}:{port}".format(host=host, port=port))
    run_server(host, port, https, server_key, server_crt)


if __name__ == '__main__':
    fake_server()