CREATE TABLE users (
  ID    INT(10) NOT NULL,
  username char(100),
  password char(256),
  join_date DATE,
  last_msg_date DATETIME,
  theme INT(10),
  PRIMARY KEY (ID)
)

SELECT * FROM users
  WHERE ID >= 0 AND ID < 100;

INSERT INTO users
  VALUES(1337,
         'DMendel',
         'theMEndel',
         '2003-01-30',
         NULL,
         'tapirs');

UPDATE users
  SET last_msg_date = NOW
  WHERE username = 'DMendel';

DELETE FROM users
  WHERE username = 'AnWakeFi';

SELECT FROM users last_msg_date, theme
  WHERE username = 'mariecur';
