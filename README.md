# Lecture_Docker

Dockerを使ってみるだけのリポジトリ

## Dockerとは

コンテナ型の仮想環境を作成・配布・実行するためのもの

![仮想環境のイメージ図](https://user-images.githubusercontent.com/91645837/211927857-727908ff-ee37-4f8a-a3df-5edd82269ab0.png)

### コンテナ型とは

ホストOSを動かしているカーネルを利用して、あたかもゲストOSがあるように仮想環境を作成する。
コンテナ型でない仮想環境の例として、仮想マシンが挙げられる。VirtualBox等の仮想マシンでは、ホストOS上で仮想化ソフト(Hypervisor等)を利用しゲストOSを動かす。その上でミドルウェアなどを動かす。そのうえでコンテナはホストマシンのカーネルを利用し、プロセスやユーザなどを隔離しつつミドルウェアを別のマシンで動かしているように見せられる。ホストマシンのカーネルを利用するため、軽量で高速に起動、停止が可能である。

![コンテナ型と仮想マシンの比較画像](https://user-images.githubusercontent.com/91645837/211934702-1cab6257-033a-41f4-a55d-da89319a3dc8.png)

### Dockerのメリット

- どのコンピュータ上でも全く同じ環境を作り出すことができる。
- 作成した環境を配布しやすい。
- スクラップ＆ビルドが容易にできる。

## Dockerのインストール

Dockerのインストールは公式サイトから行うことができます。

- [Docker公式ページ](https://www.docker.com/)
- [インストール方法(公式)](https://matsuand.github.io/docs.docker.jp.onthefly/get-docker/)

Dockerがインストールされているか確認するにはターミナルで以下を実行

```bash
docker --version
```

## Dockerを使ってみる

今回はコンテナをPullしてから起動、停止までの流れを行う。

### イメージのPull

[DockerHub](https://hub.docker.com/)のページでMySqlを検索

![検索時の画像](https://user-images.githubusercontent.com/91645837/211936125-20318254-f45d-4d5e-b62e-f4ca070b3416.png)

mysqlを開くとすると使用方法やサンプルコマンドなどが記載されている。
記載されているコマンドをターミナルで実行するとコンテナイメージをローカルにダウンロードできる。

```bash
docker pull mysql
```

ダウンロードされているイメージの一覧を確認するには以下のコマンドを実行

```bash
docker images
```

### コンテナの起動

コンテナを起動するためのコマンドの基本的な形式

```bash
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag
```

#### コマンドのタグの意味

- `--name` コンテナの名前を指定する
- `-p` ローカルPCのポート:コンテナ側のポートのそれぞれを設定
- `-e` コンテナの環境変数を設定する
- `-d` デタッチドモードで実行（バックグラウンドで実行）

#### 変更部分について

- `some-mysql`　コンテナに割り当てる名前
- `my-secret-pw` MySqlのrootユーザに設定するパスワード
- `tag` MySqlのバージョンを指定する：バージョンは先ほどのページのtagから確認することができる。

上記を踏まえて実行するコマンド

```bash
docker run --name lec-mysql -p 13306:3306 -e MYSQL_ROOT_PASSWORD=1q2w3e4r5t -d mysql
```

起動しているコンテナの情報を表示

```bash
docker ps
```

### コンテナの操作

コンテナの中に入るには以下のコマンドを実行

```bash
docker exec -it lec-mysql bash
```

- `-it` コンテナ内の操作を使っているコンソールから操作できる
- `exec` コンテナの中に入る
- `bash` コンテナ内でbashを利用する

#### MySqlを使用する

実際にMySqlを利用してみるが細かな説明は省く。

##### MySqlへログイン

コンテナ内で以下を実行

```bash
mysql -u root -p
```

実行後、先ほど設定したパスワードを入力することでmysqlの操作を行うことができる。

##### データベースの操作

適当なデータベースを作成しレコードを追加する

```bash
CREATE DATABASE lec_db;
```

```bash
USE lec_db;
```

```bash
CREATE TABLE users(
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    name VARCHAR(50)
    );
```

```bash
INSERT INTO users(name) values("Yubunen");
```

```bash
exit
```

### コンテナから抜ける

コンテナから抜けるには`Ctrl+Q`か以下のコマンドで抜けることができる。

```bash
exit
```

### コンテナの停止

コンテナの停止には以下のコマンドを実行する。

```bash
docker stop lec-mysql
```

以下のコマンドで停止しているコンテナを確認

```bash
docker ps -a
```

- `-a` 停止している者も含めすべてのコンテナを表示

### コンテナの再起動

すでに作成しているコンテナを再度実行するには以下のコマンドを実行する。

```bash
docker start lec_mysql
```

### コンテナをローカルPCで利用する

例として先ほど作成したデータベースをローカルPCのpythonで実行する

#### Pythonスクリプトの作成

以下の内容のPythonスクリプトを作成し実行する。

```python
import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='1q2w3e4r5t',
    host='localhost',
    port='13306'
)
cursor = cnx.cursor()
cursor.execute('SELECT * FROM lec_db.users')

for id, name in cursor:
    print(f'{id}: {name}')

cursor.close()
```

先ほどレコードに登録した情報が表示されればOK

### コンテナの削除

コンテナを`stop`で停止したのち、以下でコンテナを削除できる

```bash
docker rm lec-mysql
```

### イメージの削除

コンテナイメージを削除するには以下のコマンドを実行

```bash
docker rmi mysql
```

削除されているか`images`で確認できる

``` bash
docker images
```