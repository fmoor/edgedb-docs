%:
	find doc -name '*.rst' | xargs touch
	$(MAKE) -C doc $@ SPHINXOPTS="-W -n" BUILDDIR="../_build"
