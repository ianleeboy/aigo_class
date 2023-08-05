from flask import Flask, request, abort

from events.basic import *
from line_bot_api import *

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message_text = str(event.message.text).lower()

    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
