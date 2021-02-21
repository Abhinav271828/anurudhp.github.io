# All
all: haskell-blogs

# Haskell Blogs from LHS
LITERATE_HASKELL_SRCS := $(wildcard blogs/*.lhs)
LITERATE_HASKELL_BLOGS := $(pathsubst %.lhs,%.md,$(LITERATE_HASKELL_SRCS))

haskell-blogs: $(LITERATE_HASKELL_BLOGS)

%.md: %.lhs
	./scripts/lhs_to_md.sh $^ $@

