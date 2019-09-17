#!/usr/bin/env python
import argparse
import os
import functools 
from shutil import copyfile, rmtree
from yant import Server, get_fs_path, get_resource_path

def main():
    parser = argparse.ArgumentParser(epilog=r"""
Types of files

   Static
    Files that don't end in .md will be served as static files, so you can keep
    your images, css, and javascript in the same folders as your notes.

   Content
    Markdown (.md) files will be converted to HTML, and then passed to the
    appropriate template as the {{ __body__ }} field. You can add Jekyll-style 
    frontmatter by adding "---" to the top of your document, and "---\n" after
    the frontmatter has ended.

   Context
    manifest.yml files in the current and parent directories will be "inherited"
    to provide their values to the template. For example, if the current 
    directory includes color: "#fff", then the value of {{ color }} will be 
    "#fff". Note that YAML uses # as the comment character, so hex colours must
    be surrounded in quotes as shown. The quotes will not be included when the 
    value is substitued into the template. Manifests in deeper directories take
    precedence over ones further up the directory tree. Values defined in the 
    frontmatter take the highest precedence.
    In addition to the {{ __body__ }} variable, Yant provides several other 
    special variables, each surrounded in double underscores to set them apart:
    {{ __date__ }}: Date and time in ISO8601 format
    {{ __version__ }}: Version of Yant
    {{ __context__ }}: Entire context object as a pretty JSON string

   Templates
    You can put Jinja2 templates anywhere in the directory structure. The value
    {{ __template__ }} decides which template file to use. References are 
    always relative to the base directory. If basedir/subdirectory/content.md
    specifies "template: default.jinja2", then the template located at 
    basedir/default.jinja2 will be used.
    
""", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("basedir", type=str, help="path to directory containing notes")
    parser.add_argument("--port", "-p", type=int, default=8000, help="port listen on (default 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="IP address to bind to (default 127.0.0.1 - only accessible locally)")
    parser.add_argument("--freeze", type=str, metavar="DESTDIR", help="Export a rendered copy of the basedir to DESTDIR, suitable for serving statically.")
    parser.add_argument("--copy-special", action='store_true', help="When used with --freeze, copies .jinja2 and .yml files to DESTDIR")
    parser.add_argument("--force-empty", action='store_true', help="When used with --freeze, will empty DESTDIR before use")
    parser.add_argument("--livereload", "-l", action='store_true', help="Watches basedir and reloads the browser when files change.")
    args = parser.parse_args()

    if args.freeze is not None:
        freeze(args.basedir, args.freeze, copy_special=args.copy_special, force_empty=args.force_empty)
        exit(0)

    s = Server(args.basedir)
    s.start(port=args.port, host=args.host, livereload=args.livereload)


def freeze(src, dest, copy_special=False, force_empty=False):
    if not os.path.exists(dest):
        # dest does not exist, we should create it
        os.mkdir(dest)
    elif not os.path.isdir(dest):
        print(dest, " is not a directory!")
        exit(1)
    elif len(os.listdir(dest)) > 0:
        if force_empty:
            for fn in map(lambda f: os.path.join(dest,f), os.listdir(dest)):
                if os.path.isdir(fn):
                    rmtree(fn)
                else:
                    os.remove(fn)
        else:
            print(dest, " is not empty!")
            exit(2)

    # dest now exists and is an empty directory
    s = Server(src)
    r = s.renderer

    with s.app.app_context(): # https://stackoverflow.com/a/50927259
        for root, dirs, files in os.walk(src):
            print(root)
            def mkrel(path):
                raise Exception("mkrel!")
                path = path.replace(src, "", 1)
                return path[1:] if path.startswith("/") else path
            
            fs_path = functools.partial(get_fs_path, dest)
            res_path = functools.partial(get_resource_path, src)

            for d in dirs:
                os.mkdir(fs_path(res_path(os.path.join(root, d))))

            for f in files:
                if f.endswith(".md"):
                    filename = fs_path(res_path(os.path.join(
                        root, f[:-2] + "html"
                    )))

                    with open(filename, 'w') as fd:
                        fd.write(r.render(
                            res_path(os.path.join(root, f))
                        ))
                    print(" Rendered ", filename)
                elif (f.endswith(".jinja2") or f.endswith(".yml")):
                    if copy_special:
                        copyfile(os.path.join(root, f), fs_path(res_path(os.path.join(root, f))))
                        print(" Copied   ", fs_path(res_path(os.path.join(root, f))))
                else:
                    copyfile(os.path.join(root, f), fs_path(res_path(os.path.join(root, f))))
                    print(" Copied   ", fs_path(res_path(os.path.join(root, f))))

if __name__ == "__main__":
    main()
