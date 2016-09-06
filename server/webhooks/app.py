import logging
import DB
import json
from flask import Flask, request

logging.basicConfig(filename='debug.log',level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def hello():
    return json.dumps(DB.get_webhooks_updates(), indent=4, separators=(',', ': '))

@app.route("/webhooks", methods=['get'])
def webhooks_setup():
    return request.args.get('hub.challenge')

@app.route("/webhooks", methods=['post'])
def webhooks_receive():
    json = request.get_json()
    logging.info(json)
    DB.save_webhooks_update(json)
    return ''

@app.route("/webhooks_backup", methods=['get'])
def webhooks_backup_setup():
    return request.args.get('hub.challenge')

@app.route("/webhooks_backup", methods=['post'])
def webhooks_backup_receive():
    json = request.get_json()
    logging.info(json)
    DB.save_webhooks_update(json)
    return ''


if __name__ == "__main__":
    app.run()
