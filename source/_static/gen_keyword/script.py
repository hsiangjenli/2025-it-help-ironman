import pandas as pd
from jinja2 import Template

# def format_abbreviation(abbreviation):
#     return abbreviation.upper()


def format_keyterm(keyterm):
    # each word is capitalized
    return " ".join([word.capitalize() for word in keyterm.split()])


def format_description(description):
    # first letter is capitalized
    # last character is period
    if description[-1] != ".":
        description += "."
    return description.capitalize()


with open("source/_static/gen_keyword/template.rst") as f:
    rst_template = Template(f.read())

keyterms = pd.read_csv("source/_static/gen_keyword/terminology.csv")
keyterms.sort_values(by="Abbreviation", inplace=True)

# keyterms['Abbreviation'] = keyterms['Abbreviation'].apply(format_abbreviation)
keyterms["Term"] = keyterms["Term"].apply(format_keyterm)
keyterms["Definition"] = keyterms["Definition"].apply(format_description)

keyterms.to_csv("source/_static/gen_keyword/terminology.csv", index=False)

with open("source/terminology.rst", "w") as f:
    f.write(rst_template.render(keyterms=keyterms.to_dict(orient="records")))
