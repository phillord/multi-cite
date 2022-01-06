__version__ = '0.1.0'

from panflute import run_filters
from . import pubmed
from . import doi
from .util import eprint

def main(doc=None):
    f = run_filters(
        [
            bib.bib_filter,
            doi.doi_filter,
            pubmed.pubmed_filter
        ],
        doc=doc
    )
    return f
