from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def register(request):
    """
    シンプルなユーザー登録:
        - username / password は UserCreationForm
        - email は別inputで受け取り保存
    テンプレート: templates/users/register.html を想定
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email = (request.POST.get("email") or "").strip().lower()

        # email の重複チェック（簡易）
        if form.is_valid():
            if email and User.objects.filter(email__iexact=email).exists():
                form.add_error(None, "このメールアドレスは既に登録されています。")
            else:
                user = form.save()
                if email:
                    user.email = email
                    user.save(update_fields=["email"])
                login(request, user)
                return redirect("home")  # プロジェクト側で name="home" を用意してね
    else:
        form = UserCreationForm()

    return render(request, "users/register.html", {"form": form})
