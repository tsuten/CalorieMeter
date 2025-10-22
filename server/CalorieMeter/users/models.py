import os
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# avatarの保存パス: ユーザーごとにディレクトリ分け、UUID名で保存
def user_avatar_path(instance, filename):
    ext = (os.path.splitext(filename)[1] or ".bin").lower()
    return f"avatars/users_{instance.pk}/{uuid.uuid4().hex}{ext}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    daily_kcal = models.PositiveIntegerField(default=2000, help_text="1日の目標(kcal)")
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Profile({self.user.user_email})"


# 作成時に自動で空のプロフィールを付与
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, "profile"):
        Profile.objects.get_or_create(user=instance)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_email, password, **extra_fields):
        if not user_email:
            raise ValueError("メールアドレス(user_email)は必須です。")
        email_norm = self.normalize_email(user_email)
        user = self.model(user_email=email_norm, **extra_fields)
        user.set_password(password)  # ハッシュ化
        user.save(using=self._db)
        return user

    def create_user(self, user_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(user_email, password, **extra_fields)

    def create_superuser(self, user_email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(user_email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    カスタムユーザー
    - ログインID: user_email
    - 表示名: user_username（任意）
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        help_text="ログインに使用するメールアドレス",
    )
    user_username = models.CharField(
        _("username"),
        max_length=80,
        blank=True,
        help_text="画面に表示する名前（任意）",
    )
    bio = models.TextField(_("bio"), blank=True, default="")
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "user_email"
    REQUIRED_FIELDS: list[str] = []  # createsuperuser で追加項目なし

    class Meta:
        db_table = "auth_custom_user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.user_username or self.user_email
        