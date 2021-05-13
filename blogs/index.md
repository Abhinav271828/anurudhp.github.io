---
title: Blogs
layout: blog_index
---

{% assign blogs = site.pages | where: "blog", true | where_exp: "page", "page.path contains '.md'" | sort: "created" | reverse %}

{: reversed="reversed"}
{% for blog in blogs %}
0. **[{{ blog.title }}]({{ blog.url }})**
{% endfor %}
