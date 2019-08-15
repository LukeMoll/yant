from distutils.core import setup

setup(
    name="Yant",
    version="1.4",
    description="Yet Another Note Taker - Markdown and Jinja templating for your notes",
    author="Luke Moll",
    url="https://github.com/lukemoll/yant",
    packages=["yant"],
    install_requires=[
        "markdown2",
        "Jinja2",
        "flask",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "yant=yant.__main__:main"
        ]
    }
)