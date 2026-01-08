from django import template
from notifications.models import Notification
from users.models import AuthAccount
register = template.Library()

@register.inclusion_tag('header.html', takes_context=True)
def header(context):
    user = context['user']

    header_contents = [
        {"label": "Home", "label_ja": "ホーム", "icon": "home", "href": "/"},
        {"label": "Calendar", "label_ja": "カレンダー", "icon": "calendar", "href": "/calendars/m/2025/10"},
        {"label": "Statistics", "label_ja": "統計", "icon": "bar-chart-3", "href": "/statistics"},
        {"label": "History", "label_ja": "履歴", "icon": "history", "href": "/history"},
    ]

    if not user.is_authenticated:
        return {
            'header_contents': header_contents,
            'user': None,
            'user_profile': None,
            'notifications': []
        }

    from food_record.models import UserProfile
    user_profile = UserProfile.objects.filter(auth_id=user.id).first()

    notifications = (
        Notification.objects.filter(to_user=user)
        .order_by('-created_at')
    )

    return {
        'header_contents': header_contents,
        'user': user,
        'user_profile': user_profile,
        'notifications': notifications,
    }