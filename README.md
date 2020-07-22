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

ルートディレクトリにて、以下のコマンドでzip ファイルを作成する。

```
zip ../myapp.zip -r * .ebextensions
```

これで `.ebextensions` も含むようにzipファイルを作成してくれる。あとは、この `myapp.zip`をAWSのelastic beanstalkにアップロードする。
