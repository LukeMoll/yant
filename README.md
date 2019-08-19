Yant
===

*Yet another note taker*

Yant renders, templates, and serves notes written in Markdown with Jinja2 templates. It supports deep inheritance of context values.

## TODO

- [x] Put on git
- [x] Finish module setup
- [x] Move to production server instead of Flask
- [ ] More contexts:
  - [ ] Filesystem
  - [ ] Meta `{{ context }}` var, embodying whole context as JSON
  - [ ] URL query parameters? (Only needed for server side, JS can retrieve fine).
- [ ] Livereload?
- [x] `yant freeze` export to all static HTML
- [x] Documentation on Jinja variables
- [ ] Usage docs in README
- [x] Refactor to do filenames *better*
