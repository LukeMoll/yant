import os.path
import flask
from wsgiref import simple_server

from .renderer import Renderer

class Server:

    def __init__(self, baseDir):
        assert os.path.exists(baseDir), "{} does not exist".format(baseDir)
        assert os.path.isdir(baseDir), "{} is not a folder".format(baseDir)
        self.baseDir = os.path.abspath(baseDir)

        self.renderer = Renderer(baseDir)
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        def index(): return serve("/")

        @self.app.route('/<path:path>')
        def serve(path):
            print(path)
            if path.endswith("/") or path.endswith(".md"):
                path = "/" + path if path != "/" else "/"
                try:
                    return self.renderer.render(path)
                except FileNotFoundError as e:
                    return flask.abort(404)
            else:
                return flask.send_from_directory(self.baseDir, path)

    def start(self, port=8000, host="127.0.0.1"):
        with simple_server.make_server(host, port, self.app) as httpd:
            httpd.serve_forever()