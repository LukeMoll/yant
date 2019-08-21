Yant
===

*Yet another note taker*

Yant renders, templates, and serves notes written in Markdown with Jinja2 templates. It supports deep inheritance of context values.

## TODO

- [ ] More contexts:
  - [ ] Filesystem
  - [x] Meta `{{ context }}` var, embodying whole context as JSON
  - [ ] URL query parameters? (Only needed for server side, JS can retrieve fine).
  - [x] Yant `{{ version }}`, `{{ date }}`
  - [ ] `{{ git }}`?
  - [x] Move special contexts to `__` prefix (breaking)
- [ ] Livereload?
- [ ] Usage docs in README
- [x] Enable GFM tables, fenced code blocks
- [x] Checklists? (Needs custom extension)
- [x] Migrate to [python-markdown](https://github.com/Python-Markdown/markdown) to better enable future extensions
