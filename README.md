Yant
===

*Yet another note taker*

Yant renders, templates, and serves notes written in Markdown with Jinja2 templates. It supports deep inheritance of context values.

## TODO

- [ ] More contexts:
  - [ ] Filesystem
  - [ ] Meta `{{ context }}` var, embodying whole context as JSON
  - [ ] URL query parameters? (Only needed for server side, JS can retrieve fine).
  - [ ] Yant `{{ version }}`, `{{ date }}`, `{{ git }}`?
  - [ ] Move special contexts to `__` prefix (breaking)
- [ ] Livereload?
- [ ] Usage docs in README
- [ ] Enable GFM tables, checklists, fenced code blocks
- [ ] Migrate to [python-markdown](https://github.com/Python-Markdown/markdown) to better enable future extensions
