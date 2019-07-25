import os.path
import copy
import jinja2
import markdown2
import yaml

class Renderer:

    def __init__(self, baseDir):
        assert os.path.exists(baseDir), "{} does not exist".format(baseDir)
        assert os.path.isdir(baseDir), "{} is not a folder".format(baseDir)
        self.baseDir = os.path.abspath(baseDir)

        self.templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader(baseDir)
        )

        self.default_template = jinja2.Template("""<html><body>{{ body }}</body></html>""")

        self.md2 = markdown2.Markdown(extras=["metadata"])

        def normalize(path):
            if path.startswith("/"):
                return self.baseDir + path
            else: raise Exception("Invalid path: no leading /")
        self.normalize = normalize # don't need to do this like this

    def render(self, path):
        if path.endswith("/"): path += "index.md"
        manifest = self.read_manifest(path)
        html = self.read_content(path)

        context = merge({'body': html}, html.metadata, manifest)
        template = self.default_template
        if "template" in context and context["template"] is not None:
            template = self.templates.get_template(context["template"])
        return template.render(**context)

    def read_manifest(self, path):
        """Reads and inherits all the manifest.yaml files that relate to the resource at `path`
        
        Args:
            path (string): An absolute resource path --  the topmost folder is "/", equating to self.baseDir
        
        Returns:
            dict: merged dictionary of all the manifests in the tree
        """
        # I really don't like how this handles real and resource paths
        filename = self.normalize(os.path.join(os.path.dirname(path), "manifest.yaml"))

        obj = {}        
        if os.path.exists(filename):
            print("Loading", filename)
            with open(filename) as fd:
                obj = yaml.safe_load(fd)
        
        if os.path.dirname(path) == "/":
            return obj
        else:
            parentPath = os.path.abspath(os.path.join(
                os.path.dirname(path),
                os.path.pardir,
                "file" # we need a file at the end or we'll refer to the directory, not the file
            ))
            return merge(obj, self.read_manifest(parentPath))

    def read_content(self, path): 
        filename = self.normalize(path)
        with open(filename) as fd:
            return self.md2.convert(fd.read())

    def exists(self, path):
        print("?exists", path)
        norm = self.normalize(path)
        print(" n:", norm)
        return os.path.exists(norm)

def merge(*args): 
    res = {}
    args = args[::-1] # reverse arguments

    for arg in args:
        if type(arg) is not dict: continue
        for (k,v) in arg.items():
            if k in res:
                if type(v) is dict and type(res[k]) is dict:
                    res[k] = merge(v, res[k])
                else: res[k] = v
            else: res[k] = v
    
    return res
