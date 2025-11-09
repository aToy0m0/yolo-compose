from nativeauthenticator import NativeAuthenticator

c.JupyterHub.authenticator_class = NativeAuthenticator
c.NativeAuthenticator.open_signup = True
c.NativeAuthenticator.minimum_password_length = 3
c.Authenticator.admin_users = {"admin"}
c.Authenticator.allow_all = True

# DockerSpawner 設定
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Notebook イメージ
c.DockerSpawner.image = 'jupyter/minimal-notebook:latest'

# ユーザーノートブックの永続化
c.DockerSpawner.volumes = {
    '/home/ubuntu/jupyterhub_users/{username}': '/home/jovyan/work'
}

c.Spawner.default_url = '/lab'

# Hub の通信設定
c.JupyterHub.hub_ip = '0.0.0.0'
# Docker Compose ネットワーク内の jupyterhub サービス名を使って接続
c.JupyterHub.hub_connect_ip = 'jupyterhub'

# Dockerspawner で起動するノートブックコンテナも同じネットワークに参加させる
c.DockerSpawner.use_internal_ip = True
# network名は<プロジェクト名>_<論理名>
# .env で COMPOSE_PROJECT_NAME を指定している
c.DockerSpawner.network_name = 'yolo-compose_jupyterhub_net'

# タイムアウト延長
c.Spawner.start_timeout = 180
c.Spawner.http_timeout = 180

# JupyterHub ランタイムファイルの配置先
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub_data/jupyterhub_cookie_secret'
# PostgreSQL（jupyterhub_postgres）をJupyterHub DBとして利用
c.JupyterHub.db_url = 'postgresql://jhub:jhubpass@postgres:5432/jhubdb'

# カスタムテンプレートのパス設定
c.JupyterHub.template_paths = ['/srv/jupyterhub/templates']

# # サインアップとログインのURL
# http://localhost:8901/hub/signup
# http://localhost:8901/hub/login
# http://localhost:8901/hub/admin
# http://localhost:8901/hub/authorize
