from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class AddTextDirective(SphinxDirective):
    has_content = True

    def run(self):
        with open("source/sphinx_add_text/contact.html") as f:
            my_text = f.read()

        # add html content
        html_node = nodes.raw("", my_text, format="html")
        return [html_node]


def setup(app):
    app.add_directive("add_text", AddTextDirective)
    app.connect("source-read", add_text_to_h1)
    return {"version": "0.1"}


def add_text_to_h1(app, docname, source):
    lines = source[0].split("\n")
    new_lines = []
    h1_found = False

    for line in lines:
        new_lines.append(line)
        if line.startswith("=") and not h1_found:
            h1_found = True
            new_lines.append("")
            new_lines.append(".. add_text::")
            new_lines.append("")

    source[0] = "\n".join(new_lines)
