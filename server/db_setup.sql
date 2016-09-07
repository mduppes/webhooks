DROP TABLE IF EXISTS webhooks;
DROP TABLE IF EXISTS webhooks_raw;

CREATE TABLE IF NOT EXISTS webhooks (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  target_id varchar(255) NOT NULL,
  topic varchar(255) NOT NULL,
  field varchar(255) NOT NULL,
  time BIGINT NOT NULL,
  fat INT,
  value TEXT,
  raw_id INT UNSIGNED NOT NULL REFERENCES webhooks_raw(id),
  PRIMARY KEY (id),
  INDEX (time),
  INDEX (topic, field),
  INDEX (target_id)
);

CREATE TABLE IF NOT EXISTS webhooks_raw (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  value TEXT,
  PRIMARY KEY (id)
);
