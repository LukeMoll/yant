import markdown2
markdowner = markdown2.Markdown() # TODO: options in here

import jinja2
template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/', followlinks=True)
)

import flask
app = flask.Flask(__name__) # TODO: expose host and port to args

@app.route('/notes/<name>')
def notes(name):
    try:
        with open(f"notes/{name}.md") as md:
            template = template_env.get_template("notes.jinja2")
            body = markdowner.convert(md.read())
            return template.render(body=body, title=name)
    except FileNotFoundError:
        flask.abort(404)

app.run(host="localhost", port=8000)