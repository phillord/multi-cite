from panflute import *
from .util import eprint
from . import bib

def normalize_citeid_to_url(citeid):
    if citeid[0:4] == "http":
        return citeid
    if citeid[0:4] == "url:":
        return f"https://{citeid[4:]}"

    return False

def url_to_bibtex(url):
    return f'''@MISC{{url:{url},
    url =          {{{url}}},
}}'''

def resolve_and_add(url):
    url_id = f"url:{url}"
    if not bib.is_existing_ref(url_id):
        bibtex = url_to_bibtex(url)
        bib.push_to_bib(bibtex)
        bib.push_new_ref(url_id)

    return url_id

def url_filter(elem, doc):
    if type(elem) == Cite:
        for citation in elem.citations:
            if url:= normalize_citeid_to_url(citation.id):
                citation.id = resolve_and_add(url)

    return elem
