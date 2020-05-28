# up

## 環境構築

必要なもの

- docker
- docker-compose

### build

docker-compose.ymlがあるディレクトリにて以下のコマンドを叩く。

```
docker-compose up --build -d
```

### webサーバーの立ち上げ

以下のコマンドでイメージ名を探す。

```
docker ps
```

これでイメージ名が以下のように出るはず

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                               NAMES
d2377d0bfb51        mysql               "docker-entrypoint.s…"   34 minutes ago      Up 34 minutes       0.0.0.0:3306->3306/tcp, 33060/tcp   up_project_mysql_1
c25f33877ed8        up_project_django   "python3"                34 minutes ago      Up 34 minutes       0.0.0.0:8000->8000/tcp              up_project_django_1
```

以下からdjangoコンテナに入る。

```
docker exec -it up_project_django_1 /bin/bash
```

初回はマイグレーションしないといけない。

```
code# python manage.py migrate
```

マイグレーションが完了したら以下のコマンドでUpが立ち上がるはず。

```
code# python manage.py runserver 0.0.0.0:8000
```

シャットダウン方法

```
docker-compose down
```


参考にしたサイト：[docker-composeでDjangoコンテナ + MySQLコンテナの環境構築 〜 マイグレーションでテーブル作成および管理ツールで確認するまで）。](https://qiita.com/Butterthon/items/e85825d3eff6559a1cf1)
