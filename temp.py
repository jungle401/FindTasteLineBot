# APP
import googlemaps
import requests
import json

from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from linebot.models import PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate

line_bot_api = LineBotApi('DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU=')
line_bot_api.push_message('U39c4974696fe52a49832f713a9cbd648', TemplateSendMessage(
    alt_text='ButtonsTemplate',
    template=ButtonsTemplate(
        thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
        title='OXXO.STUDIO',
        text='這是按鈕樣板',
        actions=[
            PostbackAction(
                label='postback',
                data='發送 postback'
            ),
            MessageAction(
                label='說 hello',
                text='hello'
            ),
            URIAction(
                label='前往 STEAM 教育學習網',
                uri='https://steam.oxxostudio.tw'
            )
        ]
    )
))

