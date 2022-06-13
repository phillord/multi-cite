from panflute import *
from .util import eprint
import bibtexparser
import os

__bibliography_file=os.getenv("MULTICITE_BIB", "__multi_cite.bib")
__bibtex_database=None
__existing_refs=None

def is_existing_ref(refid):
    fetch_existing_refs()
    return refid in __existing_refs

def push_new_ref(refid):
    __existing_refs.add(refid)

def bibtex_database():
    global __bibtex_database
    if os.path.exists(__bibliography_file):
        with open(__bibliography_file) as bibtex_file:
            __bibtex_database = bibtexparser.load(bibtex_file)
    else:
        __bibtex_database = bibtexparser.bibdatabase.BibDatabase()

    return __bibtex_database

def fetch_existing_refs():
    global __existing_refs

    if __existing_refs == None:
        __existing_refs=set()
        for entry in bibtex_database().entries:
            __existing_refs.add(entry["ID"])

def bib_filter(elem, doc):
    ##eprint("doc", doc)
    ##eprint("type", type(doc))
    if type(elem) == MetaMap and elem.parent == doc:
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
    if new_references:
        with open(__bibliography_file, "a") as f:
            f.write(new_references)
            f.write("\n")

        eprint("Updated ", __bibliography_file)
