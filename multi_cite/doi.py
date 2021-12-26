from panflute import *
import bibtexparser
import os
import requests
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def doi_to_bibtex(doi):
    """Given a DOI fetch the relevant bibtex record"""
    r = requests.get(
        "https://doi.org/" + doi,
        headers={"Accept":"application/x-bibtex"}
    )

    bibdatabase = bibtexparser.loads(r.text)
    bibdatabase.entries[0]["ID"] = doi

    return bibtexparser.dumps(bibdatabase)

def normalize_citeid_to_doi(citeid):
    """Given a cite ID turn it into a DOI.
Return None if citeid is not a DOI"""
    if citeid[0:16] == "https://doi.org/":
        return citeid[16:]
    if citeid[0:8] == "doi.org/":
        return citeid[8:]
    if citeid[0:4] == "DOI:" or citeid[0:4] == "doi:":
        return citeid[4:]

    return None

def fetch_existing_refs(bibliography_file):
    global known_doi
    if os.path.exists(bibliography_file):
        with open(bibliography_file) as bibtex_file:
            bibtex_database = bibtexparser.load(bibtex_file)
            for entry in bibtex_database.entries:
                known_doi.add(entry["ID"])

def doi_needed(doi):
    return not doi in known_doi

def complete():
    """Complete the document"""
    if not new_references:
        return

    with open(bibliography_file, "a") as f:
        f.write(new_references)
    eprint("Updated ",bibliography_file)

##def doi_in_bibtex(doi, bibtex)
def doi_filter(elem, doc):
    global new_references
    ## TODO get this from bibliography file
    fetch_existing_refs(bibliography_file)

    if type(elem) == Cite:
        for citation in elem.citations:
            if doi := normalize_citeid_to_doi(citation.id):
                if doi_needed(doi):
                    eprint("Resolving DOI", doi)
                    new_references += doi_to_bibtex(doi)
                    known_doi.add(doi)

                citation.id=doi

    return elem

## A set of DOIs that are either in the existing .bib file or will be
## added to it at the end of the filter
known_doi=set()

## New references to add to the bibfile
new_references=""

## The bibfile
bibliography_file="__from_DOI.bib"
