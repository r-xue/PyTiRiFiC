# -*- coding: utf-8 -*-

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    'sphinx.ext.intersphinx']

from gmake import __version__

templates_path = ['_templates']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'GMaKE'
copyright = '2019, Rui Xue'
author = 'Rui Xue'


version = __version__
release = __version__

language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','tmp']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

#rst_epilog = """
#.. _Astropy: http://astropy.org
#"""
# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

#import astropy_sphinx_theme
#html_theme_path = astropy_sphinx_theme.get_html_theme_path()
#html_theme = 'bootstrap-astropy'

import sphinx_rtd_theme
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logotext1': 'GMaKE',  # white,  semi-bold
    'logotext2': '',  # orange, light
    'logotext3': ':'+__version__,   # white,  light
    'astropy_project_menubar': False
    }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

html_sidebars = {
    '**': ['localtoc.html'],
    'search': [],
    'genindex': [],
    'py-modindex': [],
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'AstropyPackageTemplatedoc'


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None,
                       'http://docs.astropy.org/en/stable/': None}
                       
verbatimwrapslines = False                       
html_show_sourcelink = False
