
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.shortcuts import render, redirect

AuthAccount = get_user_model()



@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        display_name = (request.POST.get("display_name") or "").strip()  # ※今は保存しない（初回ログインで入力）
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""

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
            return render(request, "users/register.html")

        # エラーが無ければ作成を試みる（重複メールはここで弾く）
        try:
            user = AuthAccount.objects.create_user(email=email, password=password1)
        except IntegrityError:
            messages.error(request, "このメールアドレスは既に登録されています。")
            return render(request, "users/register.html")

        login(request, user)

        if display_name:
            request.session["first_login_prefill_display_name"] = display_name

        messages.success(request, "登録しました。")
        return redirect("first_login:check")

    # GET
    return render(request, "users/register.html")
