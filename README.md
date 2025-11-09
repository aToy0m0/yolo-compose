# yolo-compose

Docker Compose で JupyterHub + PostgreSQL を起動するための最小セット。
このディレクトリ単体で完結するため、リポジトリをクローンしたら本フォルダに移動して以下の手順どおりに実行する。

## 前提条件
- Docker 24 以降 / Docker Compose v2 以降
- `stat` や `sudo` が利用できる Linux (WSL2 含む)
- コンテナイメージをビルドできるネットワーク接続

## 初回セットアップ
1. リポジトリを取得して移動する
   ```bash
   git clone https://github.com/aToy0m0/yolo-compose.git
   cd yolo-compose
   ```
2. `.env` を確認し、ホストの Docker ソケットの GID を設定する
   ```bash
   stat -c '%g' /var/run/docker.sock
   # 出力値を DOCKER_GID=xxx に書き換える
   ```
   ```
   stat -c '%g' /var/run/docker.sock は、そのファイル（Docker デーモンの UNIX ソケット）に設定されている「グループ ID (GID)」を数値で返します。
   ソケットを所有しているグループが誰かを知るためのものです。

   この GID はホストごとに異なりますが、通常は頻繁に変わりません。
   Docker をインストールし直したり、/var/run/docker.sock の所有グループを手動で変更しない限り固定です。
   ただし別のマシンや VM では別の値になるので、環境が変わればその都度確認する必要があります。

   設定する理由は、JupyterHub コンテナ（内の jovyan ユーザー）がホストの Docker デーモンにアクセスできるようにするためです。
   docker-compose.yml で /var/run/docker.sock をマウントしていますが、ソケットのグループ ID と同じ GID をコンテナ側に伝えないと、Dockerspawner が Permission denied を起こして Notebook コンテナを生成できません。
   そこで .env の DOCKER_GID=<stat で得た値> を使って group_add に渡し、コンテナ内ユーザーをそのグループに追加してアクセス権を合わせています。
   ```
   `COMPOSE_PROJECT_NAME` を変更する場合はここで合わせて編集する。
3. 永続ディレクトリを作成し、Hub が書き込める権限を与える
   ```bash
   mkdir -p data/jupyterhub data/postgres
   sudo chown -R 1000:100 data/jupyterhub
   ```
4. (任意) 既存の `.env` や `jupyterhub_config.py` を編集して認証方式・ボリューム・ポートを調整する。

## 起動と利用
- ビルド + 起動
  ```bash
  docker compose up -d
  ```
- 動作確認とログ
  ```bash
  docker compose ps
  docker compose logs -f jupyterhub
  ```
- JupyterHub へのアクセス: ブラウザで `http://localhost:8901` (リモートの場合はホスト IP) を開く。
  NativeAuthenticator のサインアップ画面からユーザーを登録すると即時ログイン可能。

## 各種管理用URL
### サインアップ
http://localhost:8901/hub/signup
### ログインのURL
http://localhost:8901/hub/login
### 管理画面のURL
http://localhost:8901/hub/admin
### ユーザー承認画面のURL(本リポジトリの設定では自動承認)
http://localhost:8901/hub/authorize

## その他コマンド
- Hub コンテナにシェルで入る
  ```bash
  docker compose exec jupyterhub bash
  ```
- PostgreSQL へ入る
  ```bash
  docker compose exec postgres psql -U jhub -d jhubdb
  ```

## 停止・更新
- 通常停止: `docker compose down`
- ボリュームも含めて完全に作り直す場合: `docker compose down -v` (データ消失に注意)
- 設定を変更したあと再適用する場合は `docker compose up -d --build` を再実行する。

## ディレクトリ構成メモ
- `Dockerfile`: JupyterHub コンテナをビルドするためのレシピ
- `docker-compose.yml`: postgres + jupyterhub のサービス定義
- `jupyterhub_config.py`: NativeAuthenticator と DockerSpawner の設定
- `postgres/`: Postgres 用 Dockerfile と `postgresql.conf`/`pg_hba.conf`
- `templates/`: Hub のカスタムテンプレート (例: `header.html`)
- `data/`: ホストに永続化するボリューム (`data/.gitkeep` 以外は git ignore)

## よく使うメンテナンスコマンド
```bash
# Hub ログの tail
docker compose logs -f jupyterhub

# Postgres ログ
docker compose logs -f postgres

# 生成された Notebook コンテナの一覧 (ホスト側)
docker ps --filter label=com.docker.compose.project=$(basename "$PWD")
```

必要に応じて `jupyterhub_config.py` の `c.DockerSpawner.network_name` や `.env` の `COMPOSE_PROJECT_NAME` を同じ値に揃えること。
