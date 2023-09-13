from line_bot_api import *

def about_us_event(event):
    emoji = [
        {
            "index": 0,
            "productId": "5ac21e6c040ab15980c9b444",
            "emojiId": "004"
        },
        {
            "index": 19,
            "productId": "5ac22e85040ab15980c9b44f",
            "emojiId": "027"
        }
    ]

    text_message = TextSendMessage(text='''$ Oh! MaMa Chicken $
-獨家特調淋醬x美式炸雞 ~~ 
                                   
      Oh!美味 ~~

-目前僅提供網路預訂 ~
-也歡迎使用LINE PAY來付款喔 ~''', emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id = '11537',
        sticker_id = '52002740'
    )

    about_us_img = 'https://i.imgur.com/hmhKNfT.jpg'

    image_message = ImageSendMessage(
        original_content_url=about_us_img,
        preview_image_url=about_us_img
    )

    line_bot_api.reply_message(
        event.reply_token,
        [text_message, sticker_message, image_message])


def location_event(event):
    location_message = LocationSendMessage(
        title='Oh! MaMa Chicken',
        address='407台中市西屯區福星路523號',
        latitude=24.177522381871487,
        longitude=120.64528369593195
    )

    line_bot_api.reply_message(
        event.reply_token,
        location_message)
