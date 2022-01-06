from . import bib
from .util import eprint
from panflute import *

import bibtexparser
import requests


def doi_to_bibtex(doi):
    """Given a DOI fetch the relevant bibtex record"""
    r = requests.get(
        "https://doi.org/" + doi,
        headers={"Accept":"application/x-bibtex"}
    )

    bibdatabase = bibtexparser.loads(r.text)
    bibdatabase.entries[0]["ID"] = "doi:" + doi

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

def doi_needed(doi):
    return not bib.is_existing_ref(doi)

def doi_filter(elem, doc):
    if type(elem) == Cite:
        for citation in elem.citations:
            if doi := normalize_citeid_to_doi(citation.id):
                prefixed_doi = "doi:" + doi
                if doi_needed(prefixed_doi):
                    eprint("Resolving DOI", doi)
                    bib.push_to_bib(doi_to_bibtex(doi))
                    bib.push_new_ref(prefixed_doi)

                citation.id=prefixed_doi

    return elem
