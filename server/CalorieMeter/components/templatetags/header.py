from django import template
from notifications.models import Notification
from users.models import CustomUser
register = template.Library()

@register.inclusion_tag('header.html', takes_context=True)
def header(context):
    header_contents = [
        {"label": "Home",
         "icon": "home",
         "href": "/"},
        {"label": "Calendar",
         "icon": "calendar",
         "href": "/calendars/m/2025/10"},
        {"label": "Statistics",
         "icon": "bar-chart-3",
         "href": "/statistics"},
        {"label": "History",
         "icon": "history",
         "href": "/history"},
    ]

    notifications = Notification.objects.filter(to_user=CustomUser.objects.get(id="f68eea44-9a37-4b44-a619-11b2c7135665")).order_by('-created_at')

    return {'header_contents': header_contents, 'notifications': notifications}