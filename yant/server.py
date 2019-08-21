import os.path
from wsgiref import simple_server
from socketserver import ThreadingMixIn
import flask
import livereload as lreload

from .renderer import Renderer

class ThreadingWSGIServer (ThreadingMixIn, simple_server.WSGIServer): pass

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
            if rpath.endswith("/") or rpath.endswith(".html") or rpath == "":
                try:
                    return self.renderer.render(rpath)
                except FileNotFoundError as e:
                    print(e)
                    return flask.abort(404)
            elif rpath.endswith(".md"):
                return flask.redirect("/{}html".format(rpath[:-2]))
            else:
                return flask.send_from_directory(self.baseDir, rpath)

    def start(self, port=8000, host="127.0.0.1", livereload=False):
        if livereload:
            live_server = lreload.Server(self.app)
            live_server.watch(self.baseDir)
            live_server.serve(port=port, host=host)
        else:
            with simple_server.make_server(host, port, self.app, server_class=ThreadingWSGIServer) as httpd:
                print("Listening on http://{}:{}".format(args.host, args.port)) # livereload prints its own
                httpd.serve_forever()