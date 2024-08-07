FROM mysql:8.0.37

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

VOLUME /var/lib/mysql
# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有することで初期化の時に実行される
COPY init.sql /docker-entrypoint-initdb.d