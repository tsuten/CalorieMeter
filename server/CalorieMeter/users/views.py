
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

User = get_user_model()


# ==== サインアップ ====
@require_http_methods(["GET", "POST"])
def register(request):
    """
    最小の登録ビュー:
      - 必須: user_email, password1, password2
      - 任意: user_username, avatar
    成功で自動ログイン → home へ
    """
    if request.method == "POST":
        user_email = (request.POST.get("user_email") or "").strip().lower()
        user_username = (request.POST.get("user_username") or "").strip()
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""
        avatar = request.FILES.get("avatar")

        # バリデーション最小
        errors = []
        if not user_email:
            errors.append("メールアドレスは必須です。")
        if not password1:
            errors.append("パスワードは必須です。")
        if password1 != password2:
            errors.append("パスワードが一致しません。")

        if not errors:
            try:
                user = User.objects.create_user(
                    user_email=user_email,
                    password=password1,
                    user_username=user_username,
                )
                if avatar:
                    user.avatar = avatar
                    user.save(update_fields=["avatar"])
                login(request, user)
                messages.success(request, "登録しました。")
                return redirect("home")
            except IntegrityError:
                errors.append("このメールアドレスは既に登録されています。")

        # エラー時
        for e in errors:
            messages.error(request, e)

    return render(request, "users/register.html")


# ==== プロフィール表示 ====
@login_required
def profile(request):
    """
    自分のプロフィールを表示（プロフィール編集導線を用意）
    """
    return render(request, "users/profile.html", {"user_obj": request.user})


# ==== プロフィール更新 ====
@login_required
@require_http_methods(["POST"])
def profile_update(request):
    """
    表示名・アバター・自己紹介の簡易更新
    フォーム側の name は:
      - user_username
      - bio
      - avatar (file)
    """
    u = request.user
    user_username = (request.POST.get("user_username") or "").strip()
    bio = (request.POST.get("bio") or "").strip()
    avatar = request.FILES.get("avatar")

    fields = []
    if user_username != u.user_username:
        u.user_username = user_username
        fields.append("user_username")
    if bio != u.bio:
        u.bio = bio
        fields.append("bio")
    if avatar:
        u.avatar = avatar
        fields.append("avatar")

    if fields:
        u.save(update_fields=fields)
        messages.success(request, "プロフィールを更新しました。")
    else:
        messages.info(request, "変更はありません。")

    return redirect("users:profile")
