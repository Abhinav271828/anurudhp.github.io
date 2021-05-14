---
title: Blogs
layout: blog_index
---

{% assign blogs = site.pages | where: "blog", true | where_exp: "page", "page.path contains '.md'" | sort: "created" | reverse %}

{: reversed="reversed"}
{% for blog in blogs %}
0. **[{{ blog.title }}]({{ blog.url }})**
   <div class="text-gray f6">{{ blog.created | date: "%B %d, %Y" }}
   {% if blog.tags %} <b>|</b> <div class="tags"> <u>&#35;{{ blog.tags | join: "</u>, <u>&#35;" }} </u> </div> {% endif %}
   </div>
{% endfor %}
