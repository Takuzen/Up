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

`rds_read_keypairs.pem`をメンバーから渡してもらう。

コマンドラインで、pemファイルが存在するディレクトリにて以下のコマンドをたたく。そうすると、以下のように出てログインできるはず。初回はいろいろ聞かれるが、`y`で答える。

```
$ ssh -i "rds_read_keypairs.pem" ec2-user@ec2-52-90-226-189.compute-1.amazonaws.com

Last login: Fri Aug  7 11:42:05 2020 from p57cabd.tokynt01.ap.so-net.ne.jp

       __|  __|_  )
       _|  (     /   Amazon Linux 2 AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-2/
4 package(s) needed for security, out of 8 available
Run "sudo yum update" to apply all updates.
-bash: warning: setlocale: LC_CTYPE: cannot change locale (UTF-8): No such file or directory
[ec2-user@ip-172-31-47-99 ~]$
```

以下のコマンドをたたく。`tkz`というユーザ名でRDSに入る。
**もし今後このレポジトリをオープンにする場合は以下のコマンドは消してください**

```
[ec2-user@ip-172-31-47-99 ~]$ mysql -h aa7ju5mn5ddy15.c6mwbzjablk2.us-east-1.rds.amazonaws.com -P 3306 -u tkz -p
password: 19960430
```

以下のように示されたらOK

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 18846
Server version: 5.7.22-log Source distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]>
```

ここから `ebdb`に入る。

```
MySQL [(none)]> use ebdb;
MySQL [ebdb]> show tables;
+-----------------------------+
| Tables_in_ebdb              |
+-----------------------------+
| app_item                    |
| auth_group                  |
| auth_group_permissions      |
| auth_permission             |
| django_admin_log            |
| django_content_type         |
| django_migrations           |
| django_session              |
| register_profile            |
| users_user                  |
| users_user_groups           |
| users_user_user_permissions |
+-----------------------------+
12 rows in set (0.00 sec)
```

これで`app_item`などをsql文でいじることが可能。

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
docker exec -it CONTAINER_NAME_DJANGO /bin/bash
# python manage.py test app
```
