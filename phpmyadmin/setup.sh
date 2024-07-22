#!/bin/sh

# phpMyAdminのインストールと設定
cd /usr/share
rm -rf phpmyadmin
unzip /tmp/phpmyadmin.zip -d /usr/share
mv /usr/share/phpMyAdmin-*-all-languages /usr/share/phpmyadmin
cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php
echo "\$cfg['blowfish_secret'] = '6vB7pN0oQ9rZ1tU4wX8yC3vB2kL5sH7y';" >> /usr/share/phpmyadmin/config.inc.php

# HTTPSを強制する設定
echo "\$cfg['ForceSSL'] = true;" >> /usr/share/phpmyadmin/config.inc.php
echo "\$cfg['Servers'][\$i]['host'] = 'mysql_fast';" >> /usr/share/phpmyadmin/config.inc.php
echo "\$cfg['Servers'][\$i]['port'] = '3306';" >> /usr/share/phpmyadmin/config.inc.php

# 重複する設定を削除して再追加
sed -i '/\$cfg\[.*SessionSavePath.*\]/d' /usr/share/phpmyadmin/config.inc.php
sed -i '/\$cfg\[.*CheckConfigurationPermissions.*\]/d' /usr/share/phpmyadmin/config.inc.php
echo "\$cfg['SessionSavePath'] = '/tmp';" >> /usr/share/phpmyadmin/config.inc.php
echo "\$cfg['CheckConfigurationPermissions'] = false;" >> /usr/share/phpmyadmin/config.inc.php

# Apache設定ファイルの更新
echo "<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /usr/share/phpmyadmin
    ServerName localhost

    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>" > /etc/apache2/sites-enabled/000-default.conf

# Apache再起動
service apache2 restart
