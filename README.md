# up

## 環境構築

必要なもの

- docker
- docker-compose

### build

docker-compose.ymlがあるディレクトリにて以下のコマンドを叩く。
これでウェブサーバーも同時に立ち上がる。

```
docker-compose up --build -d
```

### マイグレーション

以下のコマンドでイメージ名を探す。

```
docker ps
```

これでイメージ名が以下のように出るはず

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                               NAMES
4b5a9a62c503        mysql               "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        0.0.0.0:3306->3306/tcp, 33060/tcp   up_mysql_1
c846a1d071d3        up_django           "python3"                6 minutes ago       Up 6 minutes        0.0.0.0:8000->8000/tcp              up_django_1

```

以下からdjangoコンテナに入る。

```
docker exec -it up_django_1 /bin/bash
```

初回はマイグレーションしないといけない。

```
code# python manage.py migrate
```


### シャットダウン方法

```
docker-compose down
```


参考にしたサイト：[docker-composeでDjangoコンテナ + MySQLコンテナの環境構築 〜 マイグレーションでテーブル作成および管理ツールで確認するまで）。](https://qiita.com/Butterthon/items/e85825d3eff6559a1cf1)


## Deployment

### awsebcliを使う形式

brewでawsebcliをインストール（pipだと失敗）

```
$ brew install awsebcli
```

eb initで初期化

```
$ eb init
```

default regionの選択：N. Virginia

```
Select a default region
// US East (N. Virginia)us-east-1 を選択
```

aws-access-id と aws-secret-keyを入力。

```
You have not yet set up your credentials or your credentials are incorrect
You must provide your credentials.
(aws-access-id): hoge (aws consoleからとってきてください)
(aws-secret-key): hoge（aws consoleからとってきてください）
```

applicationはupを選択。

```
Select an application to use
// upを選択
```

code commitはとりあえずN。

```
Do you wish to continue with CodeCommit? (y/N) (default is n): n（defaultのまま）
```

deploy

```
//root directoryにて
$ eb deploy
```

## EC2のインスタンスに接続して、DBを変更する方法

以前はできていましたが、2020年10月時点は不具合でDBを変更できなくなっています。
近いうちに直したい。

## testコードを書くとき

### Preparation

```
$ docker exec -it up_mysql_1 /bin/bash
# mysql -u root -p

> GRANT ALL PRIVILEGES ON test_database.* TO 'DB_USER'@'%';
Query OK, 0 rows affected (0.01 sec)
````


### Executing the test codes

```
docker exec -it up_django_1 /bin/bash
# python manage.py test up.app.tests
# python manage.py test up.users.tests
```
