USE mydatabase;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_address VARCHAR(255) NOT NULL-- 型検討
);

CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    date DATE NOT NULL,
    destination VARCHAR(255) NOT NULL,
    destination_address VARCHAR(255) NOT NULL,-- 型検討
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ここから下はテスト用データ------------------testuserのパスワードはtest
INSERT INTO users (user_id, user_name, email, password, user_address)
           VALUES (1, '名古屋市役所職員', 'sample@email.com1', '$2b$12$8MZt4A8ELwcPUKOc9pUbMO1FM3/ocsHMiEUE2K0eOAuLgm8nj.HC6', '愛知県名古屋市中区三の丸３丁目１−１'),
                  (2, '清水寺の住職', 'sample@email.com2', '$2b$12$8MZt4A8ELwcPUKOc9pUbMO1FM3/ocsHMiEUE2K0eOAuLgm8nj.HC6', '京都府京都市東山区清水１丁目２９４');
INSERT INTO schedules (user_id, date, destination, destination_address)
               VALUES (1, '2024-08-31', 'ディズニーランド', '千葉県浦安市舞浜１−１'),
                      (1, '2024-10-05', '東京タワー', '東京都港区芝公園４丁目２−８'),
                      (2, '2024-09-20', '阪神甲子園球場', '兵庫県西宮市甲子園町１−８２');