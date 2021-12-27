test:
	pandoc sample1.md -t json | poetry run multi-cite | pandoc -f json -o out1.md
