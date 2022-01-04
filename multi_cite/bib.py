from panflute import *
from .util import eprint
import bibtexparser
import os

__bibliography_file="__multi_cite.bib"
__bibtex_database=None

def bibtex_database():
    global __bibtex_database
    if os.path.exists(__bibliography_file):
        with open(__bibliography_file) as bibtex_file:
            __bibtex_database = bibtexparser.load(bibtex_file)
    else:
        __bibtex_database = bibtexparser.bibdatabase.BibDatabase()

    return __bibtex_database

def bib_filter(elem, doc):
    if type(elem) == MetaMap:
        bib = elem.content.get("bibliography")
        if not bib:
            elem.content["bibliography"] = MetaList(
                MetaInlines(Str(__bibliography_file))
            )
            return elem

        if not MetaInlines(Str(__bibliography_file)) in bib:
            bib.append(MetaInlines(Str(__bibliography_file)))
            return elem

def push_to_bib(new_references):
    with open(__bibliography_file, "a") as f:
        f.write(new_references)

    eprint("Updated ", __bibliography_file)
