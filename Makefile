SPHINXOPTS:="-W -n"

%:
	find doc -name '*.rst' | xargs touch
	$(MAKE) -C doc $@ SPHINXOPTS=$(SPHINXOPTS) BUILDDIR="../_build"
