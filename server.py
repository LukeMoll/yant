import os.path
import flask

from renderer import Renderer

class Server:

    def __init__(self, baseDir):
        assert os.path.exists(baseDir), "{} does not exist".format(baseDir)
        assert os.path.isdir(baseDir), "{} is not a folder".format(baseDir)
        self.baseDir = os.path.abspath(baseDir)

        self.renderer = Renderer(baseDir)

    def start(self, port=8000):
        self.app = flask.Flask(__name__)

        @self.app.route('/')
        def index(): return serve("/")

        @self.app.route('/<path:path>')
        def serve(path):
            print(path)
            if path.endswith("/") or path.endswith(".md"):
                path = "/" + path
                if self.renderer.exists(path):
                    return self.renderer.render(path)
                else: 
                    return flask.abort(404)
            else:
                return flask.send_from_directory(self.baseDir, path)

        self.app.run(host="localhost", port=port)


if __name__ == "__main__":
    s = Server("tmp/")
    s.start()