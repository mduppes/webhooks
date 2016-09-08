import mysql.connector
import config
import json
import logging
import time

def save_webhooks_update(update):
    """Given a string update, decodes it to json and stores it if valid"""

    topic = update['object']
    entries = update['entry']

    if not topic or not entries:
        return

    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor(buffered=True)

    raw_update_id = insert_raw_webhooks_update(cursor, update)
    for entry in entries:
        fat_ping = 'changes' in entry
        target_id = entry['id']
        timestamp = entry['time']

        if fat_ping:
            for change in entry['changes']:
                value = json.dumps(change)
                field = change['field']
                insert_webhooks_update(cursor, raw_update_id, target_id, topic, timestamp, field, value)
        else:
            for field in entry['changed_fields']:
                insert_webhooks_update(cursor, raw_update_id, target_id, topic, timestamp, field, None)

    connection.commit()
    cursor.close()
    connection.close()

def insert_raw_webhooks_update(cursor, update):
    """Inserts the raw update into the raw table
    mysql> show indexes from webhooks_raw;
    +--------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    | Table        | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
    +--------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    | webhooks_raw |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    +--------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    1 row in set (0.00 sec)

    mysql> desc webhooks_raw;
    +-------+------------------+------+-----+---------+----------------+
    | Field | Type             | Null | Key | Default | Extra          |
    +-------+------------------+------+-----+---------+----------------+
    | id    | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
    | value | text             | YES  |     | NULL    |                |
    +-------+------------------+------+-----+---------+----------------+
    """

    cursor.execute(
        "INSERT INTO webhooks_raw (value, time) VALUES (%s , %s)", 
        (json.dumps(update), time.time()),
    )

    return cursor.lastrowid


def insert_webhooks_update(
    cursor,
    raw_update_id,
    target_id,
    topic,
    timestamp,
    field,
    value):
    """Inserts the parsed update into parsed table:
    mysql> desc webhooks;
    +-----------+------------------+------+-----+---------+----------------+
    | Field     | Type             | Null | Key | Default | Extra          |
    +-----------+------------------+------+-----+---------+----------------+
    | id        | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
    | target_id | varchar(255)     | NO   | MUL | NULL    |                |
    | topic     | varchar(255)     | NO   | MUL | NULL    |                |
    | field     | varchar(255)     | NO   |     | NULL    |                |
    | time      | bigint(20)       | NO   | MUL | NULL    |                |
    | fat       | int(11)          | YES  |     | NULL    |                |
    | value     | text             | YES  |     | NULL    |                |
    | raw_id    | int(10) unsigned | NO   |     | NULL    |                |
    +-----------+------------------+------+-----+---------+----------------+
    8 rows in set (0.00 sec)

    mysql> show indexes from webhooks;
    +----------+------------+-----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    | Table    | Non_unique | Key_name  | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
    +----------+------------+-----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    | webhooks |          0 | PRIMARY   |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    | webhooks |          1 | time      |            1 | time        | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    | webhooks |          1 | topic     |            1 | topic       | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    | webhooks |          1 | topic     |            2 | field       | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    | webhooks |          1 | target_id |            1 | target_id   | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
    +----------+------------+-----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
    """

    query = """
    INSERT into webhooks
        (target_id, topic, field, time, fat, value, raw_id)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (target_id, topic, field, timestamp, int(value is not None), value, raw_update_id))

def get_raw_webhooks_updates(): 
    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor()

    query = """SELECT value from webhooks_raw order by time desc limit 15"""

    cursor.execute(query)
    updates = []
    for value in cursor:
        updates.append(json.loads(value[0]))
    return updates

def get_webhooks_updates():
    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor()

    query = """SELECT target_id, topic, field, time, fat, value from webhooks order by time desc limit 10"""


    cursor.execute(query)

    items = []
    for (target_id, topic, field, timestamp, fat_ping, value) in cursor:
      items.append({
        'target_id': target_id,
        'topic': topic,
        'field': field,
        'time': timestamp,
        'fat_ping': fat_ping,
        'value': json.loads(value) if value is not None else None
      })

    cursor.close()
    connection.close()
    return items
