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
from users.models import UserProfile, OnboardingStatus, AuthAccount
from django.urls import reverse


AuthAccount = get_user_model()


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
        return redirect("users:first_login_check")


    return render(request, "register.html")


# @login_required
# def mypage(request):
#     return render(request, "mypage.html")


@login_required
def profile(request):
    
    try:
        user_profile = UserProfile.objects.get(auth=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
        return redirect("users:login")
    
    index_url = reverse("index")
    return render(request, "profile.html", {
        "profile": user_profile,
        "index_url": index_url,
    })

@require_http_methods(["GET", "POST"])
def login_view(request):

    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        user = authenticate(request, username=email, password=password)
        print("認証結果:", user)
        if user is not None:
            auth_login(request, user)
            is_admin = user.is_superuser
            print("is_admin:", is_admin)
               
            if is_admin == True:
                    print("管理者ログイン処理")
                    auth_login(request, user)
                    return redirect("index")

            else: # 通常ログイン処理
                pass

            try:
                status = OnboardingStatus.objects.get(user=user)
                print("オンボーディングステータス取得:", status)
                
            except OnboardingStatus.DoesNotExist:
                status = None
                is_admin = False
                # indexへリダイレクト

            if status.is_completed==False:
                print("初回ログイン未完了リダイレクト")
                return redirect("users:first_login_form")
            
            elif status.is_completed==True:
                print("通常ログイン処理")
                auth_login(request, user)
                next_url = request.GET.get("next") or request.POST.get("next") or "/"
                return redirect(next_url)


        messages.error(request, "メールアドレスまたはパスワードが正しくありません。")


    # print("通常ログイン画面表示:", request.method, status)
    return render(request, "login.html") # messagesも渡したい


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("users:login")