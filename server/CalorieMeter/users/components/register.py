from django_unicorn.components import UnicornView
import re


class RegisterView(UnicornView):
    email = ""
    password1 = ""
    password2 = ""
    is_password1_put = False

    def validate_email(self):
        if not self.email:
            self.add_error("email", "メールアドレスは必須です")
            return
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            self.add_error("email", "メールアドレスの形式が不正です")
            return
        return True

    def validate_password1(self):
        print("password1 validated", self.password1)
        self.is_password1_put = bool(self.password1)

    def updated_password1(self, value):
        print("password1 updated", value)
        self.is_password1_put = bool(value)

    def register(self):
        if self.password1 != self.password2:
            self.add_error("password2", "パスワードが一致しません")
            return
        self.email = self.email.lower()
        self.password1 = self.password1
        self.password2 = self.password2
        self.save()
