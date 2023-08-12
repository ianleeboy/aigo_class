from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, StickerSendMessage, ImageSendMessage, LocationSendMessage,
    FlexSendMessage, TemplateSendMessage, ImageCarouselTemplate, ImageCarouselColumn, PostbackAction
)

line_bot_api = LineBotApi('lC3x4DztwkbiuE10Thh2e15d0JXNfij2qvGkPBRgfuccrYxzmy9gkndKphWQphcIF98dJ5tPYfi1RIECue2uo98PEZhL1HfyuN3wrLqRDcOVnuAbUA3Gj3w4NtkfE42hMq9dE7L52FUd1ZDu/+egUAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('30f1790759183d5f66e968eae3ce65c0')