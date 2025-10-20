# Data Models Documentation

## ユーザー
### 認証
``` yaml
id: uuid
email: email
password: string(hashed)
```

### ユーザー
``` yaml
id: uuid
auth_id: foreign
avatar: image
display_name: string
bio: string
```

<!-- todo: 体重や身長などの身体的情報を入力？ -->
### additional personal info
``` yaml
id: uuid
auth_id: foreign
```