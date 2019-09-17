import os.path
import copy
from functools import partial
import pkg_resources
import datetime

import jinja2
import yaml
import json
import markdown
from MarkdownHighlight.highlight import HighlightExtension
from markdown_checklist.extension import ChecklistExtension

from .utils import get_fs_path, get_resource_path
import sys
sys.setrecursionlimit(100)


class Renderer:

    def __init__(self, baseDir): # TODO: take Flask app argument
        assert os.path.exists(baseDir), "{} does not exist".format(baseDir)
        assert os.path.isdir(baseDir), "{} is not a folder".format(baseDir)
        self.baseDir = os.path.abspath(baseDir)
        self.fs_path = partial(get_fs_path, self.baseDir)
        self.res_path = partial(get_resource_path, self.baseDir)

        self.templates = jinja2.Environment(
            loader=jinja2.FileSystemLoader(baseDir)
        )

        self.default_template = jinja2.Template("""<html><body>{{ __body__ }}</body></html>""")

        self.md = markdown.Markdown(extensions=[
            "meta",             # Built-in extensions
            "tables", 
            "fenced_code", 
            "def_list", 
            "abbr", 
            "sane_lists",
            HighlightExtension(), # extensions from pip
            ChecklistExtension()
        ])

    def render(self, rpath : str):
        assert not rpath.startswith("/"), "rpath cannot begin with /"

        if rpath == "": rpath = "index.html"
        if rpath.endswith("/"): rpath += "index.md"
        if rpath.endswith(".html"): rpath = rpath[:-4] + "md"
        
        manifest = self.read_manifest(rpath)
        (html, meta) = self.read_content(rpath)
        meta = dict(map(lambda t: (t[0], ";".join(t[1])), meta.items()))

        context = merge({'__body__': html}, self.special_context(), meta, manifest)
        context["__context__"] = json.dumps(context, sort_keys=True, indent=4)

        template = self.default_template
        if "__template__" in context and context["__template__"] is not None:
            template = self.templates.get_template(context["__template__"])
        return template.render(**context) # TODO: replace with self.app.render_template(context["__template__"], context)

    def special_context(self):
        try:
            version = pkg_resources.get_distribution("yant").version
        except pkg_resources.DistributionNotFound as e:
            print(e) # this _really_ shouldn't happen
            version = None
        return {
            "__version__": version,
            "__date__": datetime.datetime.now().isoformat()
        }

    def read_manifest(self, rpath):
        """Reads and inherits all the manifest.yaml files that relate to the resource at `path`
        
        Args:
            rpath (string): An absolute resource path --  the topmost folder is "", equating to self.baseDir. Must not start with leading /
        
        Returns:
            dict: merged dictionary of all the manifests in the tree
        """

        filename = os.path.join(
            self.fs_path(rpath) if rpath.endswith("/") # We're referring to the folder
            else os.path.dirname(self.fs_path(rpath)), # We want the folder containing rpath
            "manifest.yaml"
        )

        obj = {}        
        if os.path.exists(filename):
            with open(filename) as fd:
                obj = yaml.safe_load(fd)
        
        if os.path.dirname(rpath) == "":
            return obj
        else:
            try:
                parentPath = self.res_path(os.path.join(
                    os.path.dirname(filename),
                    os.path.pardir
                ))
                if parentPath != "":
                    parentPath += "/" # We're referring to the folder
                
            except FileNotFoundError as e:
                print(e)
                print(rpath)
                print(filename)

            return merge(obj, self.read_manifest(parentPath))

    def read_content(self, rpath): 
        filename = self.fs_path(rpath)
        with open(filename) as fd:
            self.md.reset()
            return (self.md.convert(fd.read()), self.md.Meta)

    def exists(self, rpath):
        return os.path.exists(self.fs_path(rpath))

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
