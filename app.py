#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "show.item":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get("item")

    speech = "Showing item " + item

    print("Response:")
    print(speech)

    kik_message = [
        {
            "type": "picture",
            "picUrl": "https://github.com/trizym/nejlbot/blob/master/pictures/kram1.png?raw=true" + item +".png"
        },
        {
            "type": "picture",
            "picUrl": "https://github.com/trizym/nejlbot/blob/master/pictures/IMG_1387.png?raw=true" + item +".png"
        },
        {
            "type": "text",
            "body": "Kram <3 " + item
        }
    ]

    print(json.dumps(kik_message))

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"kik": kik_message},
        # "contextOut": [],
        "source": "apiai-kik-images"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
