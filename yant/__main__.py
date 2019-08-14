#!/usr/bin/env python
import argparse
from yant import Server

def main():
    parser = argparse.ArgumentParser(epilog=r"""
Types of files

   Static
    Files that don't end in .md will be served as static files, so you can keep
    your images, css, and javascript in the same folders as your notes.

   Content
    Markdown (.md) files will be converted to HTML, and then passed to the
    appropriate template as the {{ body }} field. You can add Jekyll-style 
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

   Templates
    You can put Jinja2 templates anywhere in the directory structure. The value
    {{ template }} decides which template file to use. References are always 
    relative to the base directory. If basedir/subdirectory/content.md 
    specifies "template: default.jinja2", then the template located at 
    basedir/default.jinja2 will be used.
    
""", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("basedir", type=str, help="path to directory containing notes")
    parser.add_argument("--port", "-p", type=int, default=8000, help="port listen on (default 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="IP address to bind to (default 127.0.0.1 - only accessible locally)")
    args = parser.parse_args()

    s = Server(args.basedir)
    s.start(port=args.port, host=args.host)

if __name__ == "__main__":
    main()
    
