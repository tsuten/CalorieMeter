from django import template

register = template.Library()

@register.inclusion_tag('header.html', takes_context=True)
def header(context):
    header_contents = [
        {"label": "Home",
         "icon": "home",
         "href": "/"},
        {"label": "Upload",
         "icon": "plus-circle",
         "href": "/upload"},
        {"label": "History",
         "icon": "history",
         "href": "/history"},
    ]

    return {'header_contents': header_contents}