# -*- coding: utf-8 -*-

import os
import sys
import shutil
import asyncio
import platform


import click
from loguru import logger
from quart import Quart, request, send_file
from hypercorn.config import Config
from hypercorn.asyncio import serve


app = Quart(__name__)

VERSION = '0.2'


def get_system():
    return platform.system()


system = get_system()


HTTP_METHODS = {'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'}
DEFAULT_HOST = '0.0.0.0' if system == 'Darwin' else '127.0.0.1'
DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
DEFAULT_SERVER_KEY = 'local_server.key'
DEFAULT_SERVER_CRT = 'local_server.crt'
HOSTS_FILE = os.path.join(os.environ['SYSTEMROOT'], 'system32/drivers/etc/hosts') if system == 'Windows' else '/etc/hosts'


def run_server(host=DEFAULT_HOST, port=DEFAULT_HTTP_PORT, https=True, server_key=DEFAULT_SERVER_KEY, server_crt=DEFAULT_SERVER_CRT):
    config = Config()
    config.bind = ["%s:%s" % (host, port)]
    asyncio.run(serve(app, config))


class HostsLine(object):
    def __init__(self, domain, ip):
        self.domain = domain
        self.ip = ip
        self.create(domain, ip)

    @classmethod
    def create(cls, domain, ip):
        """Add new line to hosts file"""
        logger.info("Redirect {domain} to {ip}".format(domain=domain, ip=ip))
        cls.backup()
        with open(HOSTS_FILE, 'a') as f:
            f.write('{ip} {domain}'.format(domain=domain, ip=ip))

    @classmethod
    def backup(cls):
        bk_file = "%s.fsbak" % HOSTS_FILE
        logger.info("Backup hosts to %s" % bk_file)
        logger.warning("Attention! Don't modify hosts file while fake_server is running!")
        shutil.move(HOSTS_FILE, bk_file)
        shutil.copy2(bk_file, HOSTS_FILE)

    @classmethod
    def restore(cls):
        bk_file = "%s.fsbak" % HOSTS_FILE
        logger.info("Restore hosts file")
        os.remove(HOSTS_FILE)
        shutil.move(bk_file, HOSTS_FILE)

    @classmethod
    def delete(cls, domain, ip):
        """Remove line from hosts file"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()


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
@click.option('--domain', required=False, help='Auto redirect domain to bind ip')
@click.option('--debug', is_flag=True, required=False, help='Output all request data for debug')
@click.version_option(VERSION, '-v', '--version')
@click.help_option('-h', '--help')
def fake_server(text, file, file_content, bind, port, server_key, server_crt, domain, https=True, debug=False):
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
    if domain:
        redirect_host = '127.0.0.1' if host == '0.0.0.0' else host
        with HostsLine(domain, redirect_host):
            run_server(host, port, https, server_key, server_crt)
    else:
        run_server(host, port, https, server_key, server_crt)


if __name__ == '__main__':
    fake_server()