from . import bib
from . import doi
from .util import eprint
from panflute import *


import xml.etree.ElementTree as ET
import requests

__entrez_slug="&email=knowledgeblog%40googlegroups.com&tool=multicite"

def pmid_to_xml(pmid):
    eprint("pmid to bibtex", pmid)
    r = requests.get(
        "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{}&db=pubmed&retmode=xml&id={}"
        .format(
            __entrez_slug,
            pmid
        )
    )

    root = ET.fromstring(r.text)

    return root


def normalize_citeid_to_pmid(citeid):
    if citeid[0:7] == "pubmed:":
        return citeid[7:]

    return None

def pmid_to_doi(pmid):
    root = pmid_to_xml(pmid)

    return root.find(".//PubmedData//ArticleIdList//ArticleId[@IdType='doi']").text

def pubmed_filter(elem, doc):
    if type(elem) == Cite:
        for citation in elem.citations:
            if pmid := normalize_citeid_to_pmid(citation.id):
                citation.id=doi.resolve_and_add(
                    pmid_to_doi(
                        pmid
                    )
                )
