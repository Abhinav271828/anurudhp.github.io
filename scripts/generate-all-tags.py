import frontmatter
import sh
from pathlib import Path

tags = []
for blog in Path('blogs/').glob('*.md'):
    data = frontmatter.load(blog)
    if 'tags' in data:
        tags += data['tags']
tags = list(set(tags))
for tag in tags:
    if not Path('blogs/tags/' + tag + '.md').exists():
        print("NEW TAG:", tag)
        sh.cp('blogs/tags/misc.md', 'blogs/tags/' + tag + '.md')

