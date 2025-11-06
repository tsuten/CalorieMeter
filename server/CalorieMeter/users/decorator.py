
from functools import wraps
from django.shortcuts import redirect 
from django.urls import reverse
from .models import UserProfile , OnboardingStatus


def login_required_chack_user_prfile(views_func):# カスタマイズ部分（関数名）
    """
    初回ログイン時の登録してない場合
    """
    
    @wraps(views_func)
    def _checker(request, *args, **kwargs):
        user = getattr(request, *args, **kwargs)

        #未ログインを回避
        if not user or not user.is_authentticated:
            return views_func(request, *args, **kwargs)
        
        #superuserとstaffを回避
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return views_func(request, *args, **kwargs)

        profile, _ = UserProfile.objects.get_or_create(auth=user)
        status, _  = OnboardingStatus.objects.get_or_create(user=user)

        #未入力があるかを判別
        missing_required =(
            not profile.display_name
            or profile.height_cm is None
            or profile.weight_kg is None
        )

        needs_onboarding = (not status.is_completed) or missing_required


        if needs_onboarding:
            request.session["onboarding_next"] = request.get_full_path()
            return redirect(reverse("first_login:form"))
        
        return views_func(request, *args, **kwargs)

    return _checker