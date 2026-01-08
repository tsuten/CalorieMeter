# food_record/unicorn/upload.py
from django_unicorn.components import UnicornView
from django.core.files.storage import default_storage
from django.utils.html import escape

class UploadView(UnicornView):
    uploaded_file = None
    message = ""

    def upload_file(self):
        """ファイルを保存してメッセージを更新"""
        if self.file:
            try:
                safe_filename = escape(self.uploaded_file.name)
                self.message = f"{safe_filename} をアップロードしました！"
                
                if hasattr(self.file, "name"):
                    default_storage.save(self.file.name, self.file)
                    self.message = f"{self.file.name} をアップロードしました！"
                else:
                    self.message = "アップロードされたファイルに名前がありません。"
            except Exception as e:
                self.message = f"ファイルのアップロード中にエラーが発生しました: {str(e)}"
        else:
            self.message = "ファイルが選択されていません。"
