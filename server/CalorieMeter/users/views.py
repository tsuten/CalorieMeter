from django.contrib import messages
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate,
    get_user_model,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.shortcuts import render, redirect

AuthAccount = get_user_model()

def index(request):  # ログアウト時に遷移
    return render(request, "index.html")

@require_http_methods(["GET", "POST"])
def register(request):

    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        display_name = (request.POST.get("display_name") or "").strip()  # ※今は保存しない（初回ログインで入力）
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""
        print("登録処理:", email, display_name, password1, password2)

        errors = []
        if not email:
            errors.append("メールアドレスは必須です。")
        if not password1:
            errors.append("パスワードは必須です。")
        if password1 != password2:
            errors.append("パスワードが一致しません。")

        # ここでエラーを弾いて即戻る（early return）
        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, "register.html")

        # エラーが無ければ作成を試みる（重複メールはここで弾く）
        try:
            user = AuthAccount.objects.create_user(email=email, password=password1)
        
        except IntegrityError:
            messages.error(request, "このメールアドレスは既に登録されています。")
            return render(request, "register.html")

        auth_login(request, user)

        if display_name:
            request.session["first_login_profile_display_name"] = display_name

        messages.success(request, "登録しました。")
        return redirect("/")


    return render(request, "register.html")


@login_required
def mypage(request):
    return render(request, "mypage.html")


@login_required
def profile(request):
    from users.models import UserProfile
    from django.urls import reverse
    
    try:
        user_profile = UserProfile.objects.get(auth=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    mypage_url = reverse("users:mypage")
    return render(request, "profile.html", {
        "profile": user_profile,
        "mypage_url": mypage_url,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:mypage")

    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get("next") or request.POST.get("next") or "/"
            return redirect(next_url)

        messages.error(request, "メールアドレスまたはパスワードが正しくありません。")

    return render(request, "login.html")


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("users:login")