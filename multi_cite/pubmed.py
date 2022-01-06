from . import bib
from .util import eprint
from panflute import *


import xml.etree.ElementTree as ET
import requests

__entrez_slug="&email=knowledgeblog%40googlegroups.com&tool=multicite"

def pmid_to_bibtex(pmid):
    eprint("pmid to bibtex", pmid)
    r = requests.get(
        "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{}&db=pubmed&retmode=xml&id={}"
        .format(
            __entrez_slug,
            pmid
        )
    )

    root = ET.fromstring(r.text)

    authors=[]
    for auth in root.findall(".//AuthorList/Author"):
        authors.append (
            auth.find("ForeName").text +
            " " + auth.find("LastName").text
        )

    authors = " and ".join(authors)
    title = root.find(".//ArticleTitle").text
    year = root.find(".//ArticleDate").find(".//Year").text

    journal_title = root.find(".//Journal/Title").text
    reported_doi = root.find(".//ELocationID").text

    pre="pubmed:"

    bibtex = f"""
@misc{{{pre}{pmid},
    author = {{{authors}}},
    title = {{"{title}"}},
    year = "{year}",

    journal={{{journal_title}}},
    doi={{{reported_doi}}},

    url = "http://www.ncbi.nlm.nih.gov/pubmed/{pmid}"
}}
    
    """
    eprint(bibtex)
    return bibtex


def normalize_citeid_to_pmid(citeid):
    if citeid[0:7] == "pubmed:":
        return citeid[7:]

    return None

def pmid_needed(pmid):
    return not bib.is_existing_ref(pmid)

def pubmed_filter(elem, doc):
    if type(elem) == Cite:
        eprint(elem)
        for citation in elem.citations:
            if pmid := normalize_citeid_to_pmid(citation.id):
                prefixed_pmid = "pubmed:" + pmid
                if pmid_needed(prefixed_pmid):
                    eprint("Resolving PMID", pmid)
                    bib.push_to_bib(pmid_to_bibtex(pmid))
                    bib.push_new_ref(prefixed_pmid)

                citation.id=prefixed_pmid

    return elem
