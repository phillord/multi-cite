from panflute import *
from . import url
from .util import eprint

def normalize_citeid_to_arxiv(citeid):
    if citeid[0:6] == "arxiv:":
        return citeid[6:]

    return None

def arxiv_to_url(arxiv):
    return f"https://arxiv.org/abs/{arxiv}"

def arxiv_filter(elem, doc):
    if type(elem) == Cite:
        for citation in elem.citations:
            if arxiv := normalize_citeid_to_arxiv(citation.id):
                citation.id=url.resolve_and_add(
                    arxiv_to_url(citation.id)
                )
