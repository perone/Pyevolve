"""
    Tooltip Sphinx extension

    :copyright: Copyright 2010 by Christian S. Perone
    :license: PSF, see LICENSE for details.

"""
from sphinx.util.compat import Directive
from docutils import nodes
import re

def tip_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    matches = re.match("\<(?P<word>\w+)\> (?P<tip>.*)", text)
    matches_tuple = matches.group("tip"), matches.group("word")
    template = """<span class="ttip" title="%s">%s</span>""" % matches_tuple
    node = nodes.raw('', template, format='html')
    return [node], []

def setup(app):
    app.add_role('tip', tip_role)