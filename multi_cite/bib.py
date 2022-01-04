from panflute import *
from .util import eprint
import bibtexparser
import os

bibliography_file="__multi_cite.bib"
bibtex_database=None
def bibtex_database():
    if os.path.exists(bibliography_file):
        with open(bibliography_file) as bibtex_file:
            bibtex_database = bibtexparser.load(bibtex_file)

    return bibtex_database

def bib_filter(elem, doc):
    if type(elem) == MetaMap:
        bib = elem.content.get("bibliography")
        if not bib:
            elem.content["bibliography"] = MetaList(
                MetaInlines(Str(bibliography_file))
            )
            return elem

        if not MetaInlines(Str(bibliography_file)) in bib:
            bib.append(MetaInlines(Str(bibliography_file)))
            return elem

def push_to_bib(new_references):
    with open(bibliography_file, "a") as f:
        f.write(new_references)

    eprint("Updated ",bibliography_file)
