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

-- ここから下はテスト用データ------------------
INSERT INTO users (user_id, user_name, email, password, user_address)
           VALUES (1, 'name1', 'sample@email.com1', 'password1', 'address1'),
                  (2, 'name2', 'sample@email.com2', 'password2', 'address2');
INSERT INTO schedules (user_id, date, destination, destination_address)
               VALUES (1, '2024-08-31', 'ディズニーランド', '千葉県浦安市舞浜１−１'),
                      (1, '2024-10-05', '東京タワー', '東京都港区芝公園４丁目２−８'),
                      (2, '2024-09-20', '阪神甲子園球場', '兵庫県西宮市甲子園町１−８２');