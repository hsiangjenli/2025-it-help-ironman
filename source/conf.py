import os
import sys

from docutils import nodes
from sphinx.util.docutils import SphinxRole

sys.path.insert(0, os.path.abspath("."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "2025 iThome 鐵人賽"
html_title = "2025 iThome 鐵人賽"
copyright = "2025, Hsiang-Jen Li"
author = "Hsiang-Jen Li"
html_favicon = "https://hsiangjenli.github.io/static/image/ico.svg"
# release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


class TitleRefRole(SphinxRole):
    def run(self):
        bib_id = self.text
        bibfiles = self.env.domaindata["cite"]["bibdata"].data.entries
        node = nodes.raw(text=bibfiles[bib_id].fields["title"], format="html")
        return [node], []


extensions = ["sphinxcontrib.bibtex", "sphinxcontrib.pseudocode", "sphinx_proof", "myst_parser"]
bibtex_bibfiles = ["paper.bib"]
bibtex_default_style = "unsrt"

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/custom.css",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

def setup(app):
    app.add_role("title-ref", TitleRefRole())
