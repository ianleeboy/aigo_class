from flask import Flask, request, abort

from events.basic import *
from events.service import *
from line_bot_api import *

from extensions import db, migrate
from models.user import User
import os

app = Flask(__name__)

app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ianlee:B8d8LHNIQWdy1oaLyxX3Y3TmjVmw90Zq@dpg-cjbik3c5kgrc73a7i060-a.singapore-postgres.render.com/line_cp92'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)



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

    elif message_text == '@預約服務':
        service_category_event(event)


@handler.add(PostbackEvent)
def handle_postback(event):
    data = dict(parse_qsl(event.postback.data))

    if data.get('action') == 'service':
        service_event(event)



@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg = """ Welcome!! 歡迎您成為 Oh MaMa 的好友~~ 
    
我是 Chicken 小精靈

-想要知道我們有什麼餐點~還有最新的商品~
-想要透過線上預約餐點也可以透過我~

-期待您的訂餐"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)

if __name__ == "__main__":
    app.run()