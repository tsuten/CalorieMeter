
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone

from users.models import UserProfile, OnboardingStatus

def _get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(auth=user)
    return profile

def _get_or_create_onboarding_status(user):
    status, _ = OnboardingStatus.objects.get_or_create(user=user)
    return status

def _needs_onboarding(user):
    profile = _get_or_create_profile(user)
    status  = _get_or_create_onboarding_status(user)
    no_name = (not profile.display_name or profile.display_name.strip() == "")
    no_h    = (profile.height_cm is None)
    no_w    = (profile.weight_kg is None)
    not_done = (not status.is_completed)
    return not_done and (no_name or no_h or no_w)

@login_required
def check(request):
    _get_or_create_profile(request.user)
    _get_or_create_onboarding_status(request.user)
    if _needs_onboarding(request.user):
        return redirect("users:first_login_form")
    return redirect("users:mypage")

@login_required
@require_http_methods(["GET", "POST"])
def form(request):
    user    = request.user
    profile = _get_or_create_profile(user)
    status  = _get_or_create_onboarding_status(user)

    if request.method == "POST":
        display_name  = (request.POST.get("display_name") or "").strip()
        bio           = (request.POST.get("bio") or "").strip()
        height_cm_raw = request.POST.get("height_cm")
        weight_kg_raw = request.POST.get("weight_kg")
        target_weight_raw = request.POST.get("target_weight")

        errors = []

        # 表示名 必須 & ユニーク
        if not display_name:
            errors.append("ユーザー名（表示名）は必須です。")
        elif UserProfile.objects.exclude(pk=profile.pk).filter(display_name=display_name).exists():
            errors.append("このユーザー名は既に使われています。")

        # 身長・体重の数値チェック
        try:
            h = float(height_cm_raw)
            w = float(weight_kg_raw)
            if h <= 0 or w <= 0:
                errors.append("身長・体重は0より大きい値で入力してください。")
        except (TypeError, ValueError):
            errors.append("身長・体重は数値で入力してください。")

        #
        t = None
        if target_weight_raw not in (None, "",""):
            try:
                t = float(target_weight_raw)
                if t <=0:
                    errors.append("")
            
            except (TypeError , ValueError):
                errors.append("")

        #保存時に
        profile.target_weight = t
        profile.save(update_fields=["display_name","bio","height_cm","weight_kg","target_weight"])


        # 先にエラーを弾いて返す
        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, "first_login/form.html", {
                "initial": {
                    "display_name": display_name,
                    "bio": bio,
                    "height_cm": height_cm_raw,
                    "weight_kg": weight_kg_raw,
                    "target_weight":target_weight_raw,
                }
            })

        # 以降は成功パス
        profile.display_name = display_name
        profile.bio = bio
        profile.height_cm = h
        profile.weight_kg = w
        profile.save(update_fields=["display_name", "bio", "height_cm", "weight_kg"])

        status.is_completed = True
        status.completed_at = timezone.now()
        status.save(update_fields=["is_completed", "completed_at"])

        messages.success(request, "初回登録が完了しました。")
        return redirect("users:profile")

    # GET
    return render(request, "mypage.html", {
        "initial": {
            "display_name": profile.display_name or "",
            "bio": profile.bio or "",
            "height_cm": profile.height_cm or "",
            "weight_kg": profile.weight_kg or "",
            "target_weight": profile.target_weight or "",
        }
    })
