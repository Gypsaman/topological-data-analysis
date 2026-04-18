# ============================================================
#  Makefile — build paper.pdf via pandoc
#  Requires: pandoc, pandoc-crossref, a LaTeX distribution
# ============================================================

PAPER      = paper
BIB        = references.bib
OUTPUT     = $(PAPER).pdf

# Pandoc options
PANDOC     = pandoc
FLAGS      = \
	--from markdown+tex_math_dollars \
	--to pdf \
	--pdf-engine=xelatex \
	--bibliography=$(BIB) \
	--citeproc \
	--number-sections \
	--highlight-style=tango \
	-V geometry:margin=1in \
	-V fontsize=11pt \
	-V linestretch=1.15 \
	-V colorlinks=true \
	-V linkcolor=blue \
	-V citecolor=blue

.PHONY: all clean

all: $(OUTPUT)

$(OUTPUT): $(PAPER).md $(BIB)
	$(PANDOC) $(FLAGS) -o $@ $<

# Build to LaTeX source for inspection / journal submission
tex: $(PAPER).md $(BIB)
	$(PANDOC) $(FLAGS) --to latex -o $(PAPER).tex $<

clean:
	rm -f $(OUTPUT) $(PAPER).tex
