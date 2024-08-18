# TRiP-TRAIL-docker-sample

このプロジェクトは、Dockerを使用してコンテナ化されたTRiP-TRAILのサンプルアプリケーションです。
アプリケーションには、FastAPI、Nginx、MySQL、およびphpMyAdminが含まれており、すべて別々のDockerコンテナで実行されます。

## File Structure

triptrail
├── .env
├── docker-compose.yml
├── fastapi
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ └── routers
│ └── routes.py
├── mysql
│ ├── Dockerfile
│ └── data
│ └── db
├── nginx
│ ├── Dockerfile
│ ├── nginx.conf
│ └── ssl
│ ├── generate_cert.sh
│ ├── nginx-selfsigned.crt
│ ├── nginx-selfsigned.key
│ └── conf.d
│ └── reverse_proxy.conf
├── phpmyadmin
│ ├── Dockerfile
│ └── config.inc.php
└── README.md

## 使用技術

- **FastAPI**: Python 3.7+用の標準的な型ヒントに基づいたAPIを構築するためのモダンで高速なウェブフレームワーク。
- **Nginx**: 高性能なウェブサーバー、リバースプロキシサーバー、およびロードバランサー。
- **MySQL**: オープンソースのリレーショナルデータベース管理システム。
- **phpMyAdmin**: MySQLの管理をウェブ上で行うためのPHPで書かれた無料ソフトウェアツール。
- **Docker**: コンテナと呼ばれるパッケージでソフトウェアを提供するためのOSレベルの仮想化を使用するプラットフォームサービスのセット。

## セットアップ手順

1. **リポジトリのクローン**:
   ```sh
   git clone git@github.com:teamD-Hackathon2024summer/TRiP-TRAIL-docker-sample.git
   cd TRiP-TRAIL-docker-sample

環境変数の設定:
ルートディレクトリに .env ファイルを作成し、必要な環境変数を追加します。

環境変数
MY_UID=1000
MY_GID=1000
PORT_FAST=8080
PORT_MYSQL_FAST=3306
MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword
MYSQL_ROOT_PASSWORD=k6meN72tfeDxfk
MYSQL_DB_FAST=mydatabase
PORT_PMA_FAST=4081
MYSQL_HOST_FAST=mysql_fast
GMAPS_PROXY_URL=http://localhost:8080/maps-proxy?
GMAPS_API_KEY=

.envファイルに自分のGoogleMapのAPI_KEYを入力してください。
GMAPS_API_KEY=
2024/8/17追記:別の環境で使用するときはGMAPS_PROXY_URLのホスト部とポート番号を調整する必要があります

Dockerコンテナのビルドと実行:

docker-compose build
docker-compose up -d

FastAPI: http://localhost:8080
phpMyAdmin: http://localhost:4081

既知の問題とTo-Doリスト
1. phpMyAdminのリダイレクト問題
問題: http://localhost/phpmyadmin にアクセスすると404エラーが返されます。 https://localhost/phpmyadmin にアクセスすると301リダイレクトが返されます。
To-Do: phpMyAdminが正しく設定され、Nginxリバースプロキシを通じてアクセス可能であることを確認する。
2. ApacheのServerNameディレクティブ
問題: Apacheのログに「Could not reliably determine the server's fully qualified domain name」というエラーが表示されます。
To-Do: phpMyAdminコンテナのApache設定に ServerName localhost を追加する。
3. SSL証明書の自己署名エラー
問題: 自己署名証明書がSSL検証の問題を引き起こします。
To-Do: 自己署名証明書を有効なSSL証明書に置き換える。

ブラウザでは起動できなかった。
CLIであれば入ることができる。

phpMyAdminへのログインに使用するユーザー名とパスワードは、MySQLのユーザー情報に基づいています。以下の2つのアカウントがありますが、どちらを使用するかは必要な権限に応じて選択してください。

MySQLのrootユーザー
ユーザー名: root
パスワード: k6meN72tfeDxfk
このアカウントは、全てのデータベースに対するフルアクセス権を持つため、管理者作業に使用します。

アプリケーション用の一般ユーザー
ユーザー名: myuser
パスワード: mypassword
このアカウントは、一般的なデータ操作やアプリケーションでの使用に適しています。
