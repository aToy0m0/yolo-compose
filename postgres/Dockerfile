FROM postgres:17

# 設定ファイルをコピー
COPY conf/postgresql.conf /etc/postgresql/postgresql.conf
COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf

# 環境変数を指定してPostgreSQLに設定ファイルを使わせる
ENV POSTGRES_USER=jhub
ENV POSTGRES_PASSWORD=jhubpass
ENV POSTGRES_DB=jhubdb

# PostgreSQL起動時に設定ファイルを適用
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]
