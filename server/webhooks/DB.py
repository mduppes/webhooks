import mysql.connector
import config

def save_webhooks_update(update):
    """Given a string update, decodes it to json and stores it if valid"""
    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor()

    query = """INSERT into webhooks
    (target_id, topic, field, time, fat, value)
    VALUES
    ("707499519337800", "page", "feed", 1473119394, 1, '{"parent_id":"707499519337800_1069771549777260","sender_name":"GrumpyTravels","sender_id":707499519337800,"item":"like","verb":"add","created_time":1473119394,"post_id":"707499519337800_1069771549777260"}')
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def get_webhooks_updates():
    connection = mysql.connector.connect(**config.mysql)
    cursor = connection.cursor()

    query = """SELECT target_id, topic, field, time, fat, value from webhooks"""


    cursor.execute(query)

    for item in cursor:
      print("{}".format(item))

    cursor.close()
    connection.close()


get_webhooks_updates()
