FROM phpmyadmin/phpmyadmin

ENV PMA_HOST=mysql
ENV MYSQL_ROOT_PASSWORD=rootpassword

VOLUME /sessions

COPY phpMyAdmin-5.2.1-all-languages.zip /tmp/phpmyadmin.zip
COPY setup.sh /docker-entrypoint-initdb.d/setup.sh
COPY config.inc.php /etc/phpmyadmin/config.inc.php

RUN apt-get update && apt-get install -y unzip && \
    chmod +x /docker-entrypoint-initdb.d/setup.sh && \
    /docker-entrypoint-initdb.d/setup.sh
