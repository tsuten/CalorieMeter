
import os
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# アバター写真の保存先パス　権限なく登録できず
def avatar_upload_path(instance, filename):
    """
    アバター画像の保存先
    users_{auth_id}/ランダムuuid.拡張子 というパスで保存
    """
    ext = (os.path.splitext(filename)[1] or ".bin").lower()
    return f"avatars/users_{instance.auth.pk}/{uuid.uuid4().hex}{ext}"


class AuthAccountManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("メールアドレス(email)は必須です。")

        email_norm = self.normalize_email(email)

        user = self.model(email=email_norm, **extra_fields)
        user.set_password(password)  # 生パス→ハッシュ保存
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # 一般ユーザー作成。is_active以外の権限は特に持たせない
        return self._create_user(email, password, **extra_fields)

    # create_superuser
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_super=True")

        return self._create_user(email, password, **extra_fields)


class AuthAccount(AbstractBaseUser):
    """
    認証テーブル（ログイン用）
    仕様：
        - id: uuid
        - email: email
        - password: hashed string (AbstractBaseUserが持つ)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        help_text="ログインに使用するメールアドレス",
    )

    # AbstractBaseUser が password / last_login を

    is_active = models.BooleanField(default=True)  # ログイン可能フラグ
    is_staff  = models.BooleanField(default=False) # 管理サイトに入る
    is_superuser = models.BooleanField(default=False) # スーパーユーザー

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = AuthAccountManager()

    # DjangoがログインIDとして使うフィールド
    USERNAME_FIELD = "email"

    # createsuperuserを使わないなら空で
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        db_table = "auth_account"
        verbose_name = "認証アカウント"
        verbose_name_plural = "認証アカウント"

    def __str__(self):
        return self.email

    # Admin/権限用のメソッド　djangoの仕様で必須
    def has_perm(self, perm, obj=None):
        return bool(self.is_superuser)

    def has_module_perms(self, app_label):
        return bool(self.is_superuser or self.is_staff)


class UserProfile(models.Model):
    """
    プロフィール（見せる用のユーザー情報）
        - id: uuid
        - auth: AuthAccountと1対1 (外部キー = auth_id)
        - avatar: 画像
        - display_name: 表示名（ニックネーム）
        - bio: 自己紹介
        - height_cm / weight_kg / daily_kcal / target_weight: 身体データなど
    このレコードは「初回ログイン時(first_login)に作成」する。
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    auth = models.OneToOneField(
        AuthAccount,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True,
    )

    display_name = models.CharField(
        max_length=80,
        blank=True,
        help_text="アプリ内で表示される名前（ニックネーム）"
    )

    bio = models.TextField(
        blank=True,
        default="",
        help_text="自己紹介",
    )

    height_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="身長(cm)"
    )
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="体重(kg)"
    )

    daily_kcal = models.PositiveIntegerField(
        default=2000,
        help_text="1日の目標摂取カロリー(kcal)"
    )

    target_weight = models.PositiveBigIntegerField(
        
        default=0,
        help_text="目標体重の設定(kg)"
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_profile"
        verbose_name = "ユーザープロフィール"
        verbose_name_plural = "ユーザープロフィール"

    def __str__(self):
        return self.display_name or f"UserProfile({self.auth.email})"


class OnboardingStatus(models.Model):
    """
    初回ログイン時にプロフィール入力を済ませたかどうか
    - user: AuthAccountと1対1
    - is_completed: Trueならもう初回入力フローをスキップ
    """

    user = models.OneToOneField(
        AuthAccount,
        on_delete=models.CASCADE,
        related_name="onboarding_status",
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "onboarding_status"
        verbose_name = "初回登録ステータス"
        verbose_name_plural = "初回登録ステータス"

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=["is_completed", "completed_at"])

    def __str__(self):
        state = "済" if self.is_completed else "未"
        return f"Onboarding({self.user.email}): {state}"
