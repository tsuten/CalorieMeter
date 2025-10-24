from django import template

register = template.Library()

@register.inclusion_tag('header.html', takes_context=True)
def header(context):
    header_contents = [
        {"label": "Home",
         "icon": "home",
         "href": "/"},
        {"label": "Calendar",
         "icon": "calendar",
         "href": "/calendar"},
        {"label": "Statistics",
         "icon": "bar-chart-3",
         "href": "/statistics"},
        {"label": "History",
         "icon": "history",
         "href": "/history"},
    ]

    return {'header_contents': header_contents}