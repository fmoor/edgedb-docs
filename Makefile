.PHONY: html


html:
	find doc -name '*.rst' | xargs touch
	$(MAKE) -C doc html SPHINXOPTS="-W -n"
