# Documentation

## 目次
クリックすると飛びます
- [Documentation](#documentation)
  - [目次](#目次)
  - [構造](#構造)
  - [アーキテクチャ](#アーキテクチャ)
  - [サーバー起動方法](#サーバー起動方法)
  - [ドキュメント記述のルール](#ドキュメント記述のルール)
  - [コミット時の添付メッセージの書き方](#コミット時の添付メッセージの書き方)
      - [基本的な型の一覧](#基本的な型の一覧)

## 構造

``` bash
.
├── docs/                     # このreadmeあるとこ
│   └── usecase/
└── server/
    ├── CalorieMeter
    │   ├── apps
    │   │   └── [app_name]
    │   │       ├── templates/
    │   │       ├── views.py  # modelを呼び出してtemplateを返す
    │   │       ├── urls.py   # viewとURLのマッピング
    │   │       └── models.py # データモデルオブジェクトの定義 + そのオブジェクトに対する操作
    │   ├── CalorieMeter      # アプリの基盤部分
    │   │   ├── asgi.py       # 非同期サーバー関連の設定なので今回は無視
    │   │   ├── urls.py       # URLパスのマッピング
    │   │   ├── settings.py   # 名前の通りアプリの設定
    │   │   └── wsgi.py       # 今回使う同期処理サーバーの設定
    │   └── manage.py
    └── requirements.txt      # サーバーの起動に必要なモジュール
```

## アーキテクチャ
**リンクは公式 / 信頼できるドキュメントに繋がっています**
- [Django](https://docs.djangoproject.com/ja/5.2/)
  - [Django-Unicorn](https://www.django-unicorn.com/docs/)
- [JavaScript](https://developer.mozilla.org/ja/docs/Web/JavaScript)
  - [Chart.js](https://www.chartjs.org/docs/latest/)
  - [TailwindCSS](https://tailwindcss.com)
- PostgreSQL

## サーバー起動方法

``` bash
# 仮想環境の作成
python3 -m venv .venv
# 仮想環境に入る
source .venv/bin/activate
# 必要なモジュールのインストール
pip install -r requirements.txt
# djangoプロジェクト内に移動
cd server/CalorieMeter
# データベースへのマイグレート
python3 manage.py migrate
# super userの作成
python3 manage.py createsuperuser
# サーバーの起動
python3 manage.py runserver
# localhost:8000にアクセスして開発を進めてください
```

## ドキュメント記述のルール
- 階層は現在地から２段階以上下げない
- 記述は基本的に全てmarkdown、もし画像や表が欲しかったら埋め込みor画像

## コミット時の添付メッセージの書き方
[Conventional Commit](https://www.conventionalcommits.org/ja/v1.0.0/)を参考にしてお願いします
#### 基本的な型の一覧
- feat: 新機能の追加
- fix: バグの修正
- docs: ドキュメントの変更のみ
- style: 動作に影響しないフォーマットの変更
- refactor: バグ修正や機能追加を含まないコードの変更
- revert: 以前のコミットを元に戻す変更