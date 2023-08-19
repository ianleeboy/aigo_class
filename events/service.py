from line_bot_api import *
from urllib.parse import parse_qsl

from extensions import db
from models.user import User
from models.reservation import Reservation

import datetime

services = {
    1:{
        'category': '套餐',
        'img_url': 'https://i.imgur.com/rl7CRDq.jpg',
        'title': '炸雞類',
        'duration': '10min',
        'description': '主餐有炸雞、雞塊、雞翅，搭配薯條跟飲料',
        'price': 2000,
        'post_url': 'https://www.facebook.com/OhMAMAchicken/'
    },
    
    2:{
        'category': '套餐',
        'img_url': 'https://i.imgur.com/efDJWJx.jpg',
        'title': '熱狗堡',
        'duration': '10min',
        'description': '現做的熱狗堡搭配薯條',
        'price': 1000,
        'post_url': 'https://www.facebook.com/OhMAMAchicken/'
    },

    3:{
        'category': '套餐',
        'img_url': 'https://i.imgur.com/gYJcINJ.jpg',
        'title': '多人分享',
        'duration': '10min',
        'description': '與朋友一起大快朵頤的雞腿桶',
        'price': 1500,
        'post_url': 'https://www.facebook.com/OhMAMAchicken/'
    },

    4:{
        'category': '單點',
        'img_url': 'https://i.imgur.com/Y2JZOVt.jpg',
        'title': '人氣點心',
        'duration': '10min',
        'description': '造型薯條 & 特調醬',
        'price': 500,
        'post_url': 'https://www.facebook.com/OhMAMAchicken/'
    },

    5:{
        'category': '單點',
        'img_url': 'https://i.imgur.com/hmhKNfT.jpg',
        'title': '飲料',
        'duration': '10min',
        'description': '各式各樣的氣泡飲料',
        'price': 3000,
        'post_url': 'https://www.facebook.com/OhMAMAchicken/'
    }
}

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想預約的餐點類型',
        template=ImageCarouselTemplate(
        columns = [
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/vyQIdkh.jpg',
                            action=PostbackAction(
                                label= '套餐',
                                display_text= '想了解套餐內容',
                                data='action=service&category=套餐'
                            )
                ),
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/cJVuVXE.jpg',
                            action=PostbackAction(
                                label= '單點',
                                display_text= '想了解單點內容',
                                data='action=service&category=單點'
                            )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])


def service_event(event):

    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service_id in services:
            if services[service_id]['category'] == data['category']:
                service = services[service_id]
                bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service['img_url']
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": service['title'],
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": service['duration'],
                        "size": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": service['description'],
                        "margin": "lg",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"NT$ {service['price']}",
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "flex": 0
                        }
                        ],
                        "margin": "xl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service_id}",
                        "displayText": f"我想預約【{service['title']} {service['duration']}】"
                        },
                        "color": "#b28530"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "了解詳情",
                        "uri": service['post_url']
                        }
                    }
                    ]
                }
                }

                bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text='請選擇訂餐項目',
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])
    

def service_select_date_event(event):

    data = dict(parse_qsl(event.postback.data))
    
    weekday_string ={
        0: '日',
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六'
    }

    business_day = [1, 2, 3, 4, 5]

    quick_reply_buttons = []

    today = datetime.datetime.today().date()

    for x in range(1, 8):
        day = today + datetime.timedelta(days=x)

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day} ({weekday_string[day.weekday()]})',
                                      text=f'我要預約 {day} ({weekday_string[day.weekday()]}) 這天',
                                      data=f'action=confirm&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪一天?',
                                   quick_reply=QuickReply(item=quick_reply_buttons))

    line_bot_api.reply_message(
        event.reply_token,
        [text_message])


def service_select_time_event(event):
     
    data = dict(parse_qsl(event.postback.data))

    available_time = ['11:00', '12:00', '13:00', '14:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(action=PostbackAction(label=time,
                                                                    text=f'{time} 這個時段',
                                                                    data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段?',
                                   quick_reply=QuickReply(item=quick_reply_buttons))
    
    line_bot_api.reply_message(
        event.reply_token,
        [text_message])