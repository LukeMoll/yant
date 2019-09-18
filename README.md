Yant
===

*Yet another note taker*

Yant renders, templates, and serves notes written in Markdown with Jinja2 templates. It supports deep inheritance of context values.

## Installation
You can install this in a venv or at user-level if you'd prefer
```
pip install git+ssh://git@github.com/LukeMoll/yant.git
```

## Usage
Notes are located in the **base directory**. This will be the root of the webserver that Yant runs.
```
yant path/to/base/directory [--options]
```
You can change the host and port with the `--host` and `--port` arguments. To see changes as they happen, use `--livereload` to reload the webpage when files are saved.

### Freezing
To "freeze" the contents of the base directory so they can be served from a standard static web server (such as nginx), use `--freeze`. By default, templates and manifest files will not be frozen. To change this behaviour, use `--copy-special`. To empty the target directory before use, call `--force-empty`. This is especially helpful when using `--freeze` in a repeated or automated manner.

## Writing notes
There are four types of files that Yant deals with:
 - **Static** files are served normally
 - **Content** files (.md) are converted to HTML and passed to the template as the `{{ __body__ }}` field.
 - **Context** files (manifest.yaml) in the current and parent directories are combined to provide values to template fields.
 - **Template** files (.jinja2) are used to substitute the rendered Markdown and context values into. 

See `yant -h` for more details.

## TODO

- [x] Use Flask's internal Jinja instead of calling Jinja explicitly
- [ ] Add Jinja function to get context from perspective of other file (params is absolute or relative resource path)
- [ ] More contexts:
  - [ ] Filesystem
  - [ ] URL query parameters? (Only needed for server side, JS can retrieve fine).
  - [ ] `{{ git }}`?
- [ ] Use [importlib.util][1] to allow user to [add functions][2] (and extensions) from baseDir


[1]: https://stackoverflow.com/a/67692
[2]: https://stackoverflow.com/a/7226047
