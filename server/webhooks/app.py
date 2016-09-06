import logging
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    contents = request.args.get('yo')
    logging.info(contents)
    if not contents:
        contents = ''
    return contents

@app.route("/webhooks", methods=['get'])
def webhooks_setup():
    return request.args.get('hub.challenge')

@app.route("/webhooks", methods=['post'])
def webhooks_receive():
    json = request.get_json()
    logging.info(json)
    return ''

if __name__ == "__main__":
    app.run()
