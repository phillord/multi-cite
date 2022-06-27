import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def url_to_bibtex(url,citeid=None):
    if not citeid:
        citeid = f"url:{url}"


    return f'''@MISC{{{citeid},
    url =          {{{url}}},
}}'''
