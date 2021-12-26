__version__ = '0.1.0'

from panflute import run_filter
from . import doi

import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def main(doc=None):
    f = run_filter(doi.doi_filter, doc=doc)
    doi.complete()
    return f
