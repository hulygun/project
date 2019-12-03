import sphinx_bootstrap_theme

project = 'game'
copyright = '2019, Denis Tormazov'
author = 'Denis Tormazov'
release = '0.1'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo'
]
exclude_patterns = []

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = ['_static']
html_theme_options = {
    'bootswatch_theme': "flatly",
    'bootstrap_version': "3"
}
templates_path = ['_templates']


def setup(app):
    app.add_stylesheet("styles.css")