import os,json

import markdown2
markdowner = markdown2.Markdown() # TODO: options in here

import jinja2
template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/', followlinks=True)
) # we might be able to do this with template_folder kwarg on flask.Flask

import flask
app = flask.Flask(__name__) # TODO: expose host and port to args

@app.route('/notes/<path:name>')
def notes(name):
    try:
        with open(f"notes/{name}.md") as md:
            template = template_env.get_template("notes.jinja2")
            body = markdowner.convert(md.read())
            return template.render(body=body, title=name)
    except FileNotFoundError:
        print(f"notes/{name}")
        flask.abort(404)

@app.route('/js/<path:p>')
def js(p): return flask.send_from_directory("js", p)

@app.route('/api/tree/')
def tree(): return subtree("")

@app.route('/api/tree/<path:subpath>')
def subtree(subpath):
    if(not os.path.exists(f"notes/{subpath}")):
        flask.abort(404)
        return
    #else...
    def go_into(path="."):
        return {
            "path": os.path.basename(path),
            "contents": [
                entry.name if not entry.is_dir() 
                else go_into(entry.path)
                for entry in os.scandir(path)
            ]
        }
    return json.dumps(go_into(f"notes/{subpath}")["contents"])
    

app.run(host="localhost", port=8000)