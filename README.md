Multi-Cite
==========


Multi-Cite is a pandoc filter which allows you to use multiple
identifiers directly as references in Markdown.

It is current in early stages of development. It is conceptually
similar to the doi2cite. It's key advantage is that it works with more
identifiers: it should function with all DOIs (doi2cite just works
with Crossref), and pubmed IDs. When complete it will add arxiv, and
scrapped metadata from any URL via greycite.

Key disadvantage over doi2cite -- it's more complicated to use. It is
written in python because it cannot be readily implemented as a lua
filter (it uses Content Negotation for DOIs which lua filters do not
support AFAICT). I have also decided to go the route of using
dependencies rather than fit into core python, so it uses panflute and
requests.

