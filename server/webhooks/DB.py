import mysql.connector
import config
import json
import logging

import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def save_webhooks_update(update):
    """Given a string update, decodes it to json and stores it if valid"""

    topic = update['object']
    entries = update['entry']

    if not topic or not entries:
        return

    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor(buffered=True)
    
    for entry in entries:
        fat_ping = 'changes' in entry 
        target_id = entry['id']
        time = entry['time']
        
        if fat_ping:
            for change in entry['changes']:
                value = json.dumps(change)
                field = change['field']
                insert_webhooks_update(cursor, target_id, topic, time, field, value)
        else:
            for field in entry['changed_fields']:
                insert_webhooks_update(cursor, target_id, topic, time, field, None)

    connection.commit()
    cursor.close()
    connection.close()
    
def insert_webhooks_update(
    cursor,
    target_id,
    topic,
    time,
    field,
    value):
    query = """INSERT into webhooks
    (target_id, topic, field, time, fat, value)
    VALUES
    (%s, %s, %s, %s, %s, %s)
    """
    logging.info('{}{}{}{}{}{}'.format(target_id, topic, field, time, value is not None, value))
    cursor.execute(query, (target_id, topic, field, time, int(value is not None), value))

def get_webhooks_updates():
    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor()

    query = """SELECT target_id, topic, field, time, fat, value from webhooks order by time desc limit 10"""


    cursor.execute(query)

    items = []
    for (target_id, topic, field, time, fat_ping, value) in cursor:
      items.append({
        'target_id': target_id,
        'topic': topic,
        'field': field,
        'time': time,
        'fat_ping': fat_ping,
        'value': json.loads(value)
      })

    cursor.close()
    connection.close()
    return items

