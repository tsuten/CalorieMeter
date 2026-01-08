from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import redirect_to_login
from users.models import UserProfile, OnboardingStatus

def login_required_check_user_profile(view_func):
    """
    ユーザーが初回ログイン時に必須情報を入力していない場合、
    フォームにリダイレクトするデコレータ。
    セッションに保存する際に UUID や Decimal は文字列・float に変換。
    """

    @wraps(view_func)
    def _checker(request, *args, **kwargs):
        user = getattr(request, "user", None)

        # 未ログインの場合はログインページへ
        if not user or not user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        # superuser/staff は無視して元のビューへ
        if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
            return view_func(request, *args, **kwargs)

        # UserProfile を取得または作成
        profile_obj, _ = UserProfile.objects.get_or_create(auth=user)
        # OnboardingStatus を取得または作成
        status, _ = OnboardingStatus.objects.get_or_create(user=user)

        # 必要な情報をセッション用に安全な形でまとめる
        profile = {
            "auth_id": str(user.id),  # UUID を文字列に
            "display_name": profile_obj.display_name or "",
            "height_cm": float(profile_obj.height_cm) if profile_obj.height_cm is not None else None,
            "weight_kg": float(profile_obj.weight_kg) if profile_obj.weight_kg is not None else None,
            "target_weight": float(profile_obj.target_weight) if profile_obj.target_weight is not None else None,
        }
        request.session["user_profile"] = profile

        # 必須情報が未入力か、オンボーディング未完了かを判定
        missing_required = (
            not profile["display_name"]
            or profile["height_cm"] is None
            or profile["weight_kg"] is None
        )
        needs_onboarding = missing_required or not status.is_completed

        if needs_onboarding:
            # 完了後に元のページに戻れるようにセッションに保存
            request.session["onboarding_next"] = request.get_full_path()
            return redirect(reverse("users:first_login_form"))

        return view_func(request, *args, **kwargs)

    return _checker
