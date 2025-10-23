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

### 食事
``` yaml
id: uuid
uploaded_by: foreign - auth
image: image
calorie: integer
time_eaten: enum - 食べた時間
```

#### 食べた時間
朝食, 昼食, 夕食, 間食, その他