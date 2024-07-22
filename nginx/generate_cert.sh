#!/bin/bash

# SSL証明書ディレクトリの作成
mkdir -p /etc/nginx/ssl

# 自己署名証明書の生成
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx-selfsigned.key -out /etc/nginx/ssl/nginx-selfsigned.crt -subj "/CN=localhost"
