from line_bot_api import *
from urllib.parse import parse_qsl


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