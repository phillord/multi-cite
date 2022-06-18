from multi_cite import __version__
from subprocess import check_output, run
import atexit
import os

def slurp(f):
    with open(f) as x:
        return x.read()

def pandoc_clean(f):
    if os.path.exists("test_bib.bib"):
        os.remove("test_bib.bib")

    if os.path.exists(f"tests/{f}.out.md"):
        os.remove(f"tests/{f}.out.md")

def pandoc(f):
    pandoc_clean(f)
    output = check_output(
        f'export MULTICITE_BIB=test_bib.bib; pandoc -t json tests/{f} | \
        poetry run multi-cite | \
        pandoc -f json -t markdown+yaml_metadata_block --standalone | \
        pandoc --citeproc --standalone --from markdown+yaml_metadata_block+citations --to commonmark+yaml_metadata_block > tests/{f}.out.md',
        shell=True
    )
    preserve=False
    if not preserve:
        atexit.register(pandoc_clean, f)

    return f"tests/{f}.out.md"

def output_eq(f, g):
    g = "tests/" + g

    diff_out = run(
        f"diff {f} {g}", shell=True,capture_output=True
    )

    if not diff_out.returncode:
        print(diff_out.stdout)

    assert diff_out.returncode == 0

def test_doi():
    output_eq(pandoc("doi.md"), "doi_expected.md")

def test_pubmed():
    output_eq(pandoc("pubmed.md"), "pubmed_expected.md")

def test_url_raw():
    output_eq(pandoc("url.md"), "url_expected.md")

def test_url2_prefixed():
    output_eq(pandoc("url2.md"), "url2_expected.md")

def test_version():
    assert __version__ == '0.1.0'
