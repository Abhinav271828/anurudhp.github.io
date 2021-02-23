# All
all: haskell_blogs feed.rss

### Haskell Blogs from LHS
LITERATE_HASKELL_SRCS := $(wildcard blogs/*.lhs)
LITERATE_HASKELL_STUBS := $(patsubst %.lhs,%,$(LITERATE_HASKELL_SRCS))
LITERATE_HASKELL_BLOGS := $(patsubst %.lhs,%.md,$(LITERATE_HASKELL_SRCS))

haskell_blogs: $(LITERATE_HASKELL_BLOGS)

$(LITERATE_HASKELL_BLOGS): %.md: %.lhs scripts/lhs_to_md.sh scripts/getYAMLMetadata.hs
	./scripts/lhs_to_md.sh $< $@

.PHONY: haskell_blogs

### RSS Feed
BLOG_SRCS := $(wildcard blogs/*.md)
feed.rss: $(BLOG_SRCS)
	python ./scripts/genrss.py -b blogs -o $@
