import os.path
from wsgiref import simple_server
import flask

from .renderer import Renderer

class Server:

    def __init__(self, baseDir):
        assert os.path.exists(baseDir), "{} does not exist".format(baseDir)
        assert os.path.isdir(baseDir), "{} is not a folder".format(baseDir)
        self.baseDir = os.path.abspath(baseDir)

        self.renderer = Renderer(baseDir)
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        def index(): return serve("")

        @self.app.route('/<path:rpath>')
        def serve(rpath):
            if rpath.endswith("/") or rpath.endswith(".html"):
                try:
                    return self.renderer.render(rpath)
                except FileNotFoundError as e:
                    print(e)
                    return flask.abort(404)
            elif rpath.endswith(".md"):
                return flask.redirect("/{}html".format(rpath[:-2]))
            else:
                return flask.send_from_directory(self.baseDir, rpath)

    def start(self, port=8000, host="127.0.0.1"):
        with simple_server.make_server(host, port, self.app) as httpd:
            httpd.serve_forever()