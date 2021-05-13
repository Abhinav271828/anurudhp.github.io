---
title: Blogs
layout: blog_index
---

{% assign blogs = site.pages | where: "blog", true | where_exp: "page", "page.path contains '.md'" | sort: "created" | reverse %}

{: reversed="reversed"}
{% for blog in blogs %}
0. **[{{ blog.title }}]({{ blog.url }})**
   <div class="text-gray f5">Posted on: {{ blog.created | date: "%B %d, %Y" }}
   {% if blog.tags %} | Tags: <u> {{ blog.tags | join: "</u>, <u>" }} </u> {% endif %}
   </div>
{% endfor %}
