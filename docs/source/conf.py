# Configuration file for the Sphinx documentation builder.
#
# For a full list of all Sphinx configuration options see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import datetime
import importlib
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'MPL Plotter'
author  = 'Antonio López Rivera'

# Project code name
codename = 'mpl_plotter'

# Copyright
copyright = f'{datetime.datetime.now().date().strftime("%Y")}, {author}'

# Language
language = 'en'

# Obtain the project's release version, which must be stored in a
# __version__ variable inside the main project script or package.
# WARNING: the script or the package's __init__.py WILL BE RUN
# on import. 
# In the case of single-script projects, the following architecture
# is suggested:
#
#            # My single-script project
#
#            __version__ = <version of your project>
#
#            if __name__ == '__main__':
#                <body of your project>
#
file_path = os.path.realpath(__file__)                            # Obtain path of this config file
root_path = (os.sep).join(file_path.split(os.sep)[:-3])           # Obtain project root path
sys.path.insert(1, root_path)                                     # Import from root path
release = importlib.import_module(codename).__version__           # Get project version
sys.path.remove(root_path)                                        # Remove root path from search

# -- Text editing ------------------------------------------------------------

# Replacements
rst_epilog = f'''
.. |project| replace:: {project}
.. |version| replace:: {release}
.. |codename| replace:: {codename}
'''

# Custom roles
rst_prolog = '''
'''

# Cross-referencing
numfig = True
numfig_format = {'figure':     'Figure %s',
                 'table':      'Table %s',
                 'code-block': 'Listing %s',
                 'section':    'Section %s'}

# -- General configuration ---------------------------------------------------

# Set path
sys.path.insert(0, os.path.abspath('../../.'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.imgmath',             # LaTeX math
              'sphinx.ext.mathjax',             # HTML math
              'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['source/_templates']

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# A list of prefixes that are ignored for sorting the Python module index 
# (e.g., if this is set to ['foo.'], then foo.bar is shown under B, not F). 
# This can be handy if you document a project that consists of a single package. 
# Works only for the HTML builder currently. Default is [].
modindex_common_prefix = [f'{codename}.']

# -- Use package and module documentation templates with better_apidoc  --------
def run_apidoc(app):
    """Generage API documentation"""
    import better_apidoc

    better_apidoc.APP = app
    better_apidoc.main(
        [
            'better-apidoc',
            '-t',
            templates_path[0],
            '-fMeET',
            '-o',
            'source',
            f'../{codename}',
        ]
    )

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_templates/*']     # Exclude templates from rendering

# -- HTML SETTINGS -------------------------------------------------------------
root_doc = 'index'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
extensions += ['sphinx_rtd_theme']

# Logo
html_logo = f'figures/demo.png'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
}

# -- LATEX SETTINGS ------------------------------------------------------------

report_doc             = 'report'
figures                = [os.path.join(dp, f) for dp, dn, filenames in os.walk('figures') for f in filenames]
latex_additional_files = ['project.sty', 'style.sty'] + figures

latex_engine = 'lualatex'

latex_elements = {
'preamble': r'\RequirePackage{project}',
'releasename': 'Version',
'papersize': 'a4paper',
'pointsize': '11pt',
'classoptions': ',openany,oneside',
'maketitle': '\maketitle',
'tableofcontents': '',
'figure_align': 'H',
'sphinxsetup': r'''
hmargin={2cm,2cm},
vmargin={4cm,3cm},
''',
}

latex_documents = [
  (report_doc, 'main.tex', f'{project} Documentation', author, 'manual'),
]

# Document __init__ files
special_members = '__init__'

# -- Generate documentation ----------------------------------------------------
def setup(app):
    app.connect('builder-inited', run_apidoc)
