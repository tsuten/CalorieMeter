from django import template
from notifications.models import Notification
from users.models import AuthAccount
register = template.Library()

@register.inclusion_tag('header.html', takes_context=True)
def header(context):
    header_contents = [
        {"label": "Home",
         "label_ja": "ホーム",
         "icon": "home",
         "href": "/"},
        {"label": "Calendar",
         "label_ja": "カレンダー",
         "icon": "calendar",
         "href": "/calendars/m/2025/10"},
        {"label": "Statistics",
         "label_ja": "統計",
         "icon": "bar-chart-3",
         "href": "/statistics"},
        {"label": "History",
         "label_ja": "履歴",
         "icon": "history",
         "href": "/history"},
    ]
    user = context['user']
    
    if not user.is_authenticated:
        return {'header_contents': header_contents, 'user': None, 'notifications': []}

    notifications = Notification.objects.filter(to_user=user).order_by('-created_at')

    return {'header_contents': header_contents, 'notifications': notifications, 'user': user}