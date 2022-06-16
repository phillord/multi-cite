citeproc-doi:
	pandoc tests/doi.md -t json | poetry run multi-cite | pandoc -f json -t markdown+yaml_metadata_block --standalone | pandoc --citeproc --standalone --from markdown+yaml_metadata_block+citations --to commonmark+yaml_metadata_block


simple_out:
	pandoc sample1.md -t json | poetry run multi-cite | pandoc -f json -o out1.md

citeproc:
	pandoc sample1.md -t json | poetry run multi-cite | pandoc -f json -t markdown | pandoc --citeproc --standalone -t markdown
