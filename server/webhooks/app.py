import logging
import DB
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='debug.log',level=logging.DEBUG)

@app.route("/api")
def hello():
    return json.dumps(DB.get_raw_webhooks_updates(), indent=4, separators=(',', ': '))
#    return json.dumps(DB.get_webhooks_updates(), indent=4, separators=(',', ': '))

@app.route("/api/webhooks", methods=['get'])
def webhooks_setup():
    return request.args.get('hub.challenge')

@app.route("/api/webhooks", methods=['post'])
def webhooks_receive():
    json = request.get_json()
    logging.info(json)
    DB.save_webhooks_update(json)
    return ''

@app.route("/api/webhooks_backup", methods=['get'])
def webhooks_backup_setup():
    return request.args.get('hub.challenge')

@app.route("/api/webhooks_backup", methods=['post'])
def webhooks_backup_receive():
    json = request.get_json()
    logging.info(json)
    DB.save_webhooks_update(json)
    return ''

if __name__ == "__main__":
    app.run()
