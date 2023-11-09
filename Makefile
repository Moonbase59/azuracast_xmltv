# This Makefile is mainly for me, to re-format the source
# and auto-generate some documentation from it.
# It requires lots of other stuff being installed, which I have.
# You can use this as an example but you DON’T NEED IT.
#
# Indentation in this file MUST use tabs!

all: format docs docs/azuracast_xmltv.md docs/azuracast_xmltv.pdf

.PHONY: format
format:
	isort --profile black azuracast_xmltv
	black azuracast_xmltv

docs:
	mkdir docs

docs/azuracast_xmltv.md: azuracast_xmltv
	# wants .py extension for loading as module
	ln -s azuracast_xmltv azuracast_xmltv.py
	pdoc3 --pdf azuracast_xmltv > docs/azuracast_xmltv.md
	rm azuracast_xmltv.py
	rm -rf __pycache__

docs/azuracast_xmltv.pdf: docs/azuracast_xmltv.md
	pandoc --metadata=title:"azuracast_xmltv Documentation" \
	       --from=markdown+abbreviations+tex_math_single_backslash \
	       --pdf-engine=xelatex --variable=mainfont:"DejaVu Sans" \
	       --toc --toc-depth=4 --output=docs/azuracast_xmltv.pdf docs/azuracast_xmltv.md
