import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def url_to_bibtex(url):
    return f'''@MISC{{url:{url},
    url =          {{{url}}},
}}'''
