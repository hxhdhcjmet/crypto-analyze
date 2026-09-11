MAIN=main
OUTDIR=output

all:
	latexmk -xelatex -output-directory=$(OUTDIR) $(MAIN).tex

clean:
	latexmk -c -output-directory=$(OUTDIR)

cleanall:
	latexmk -C -output-directory=$(OUTDIR)

bib:
	latexmk -xelatex -bibtex -output-directory=$(OUTDIR) $(MAIN).tex