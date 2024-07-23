# google APP
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
from linebot.models import * 

from linebot.v3.messaging import MessagingApi


app = Flask(__name__)

access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
secret = 'e90e4acf2cce57e39e9c69032f23ea22'

line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
handler = WebhookHandler(secret)                     # 確認 secret 是否正確
ID=""

# ---------------------------------------------------------------------------------------------------------

def handle_text_message(event):
    msg = event.message.text
    tk = event.reply_token

    if msg == '特定訊息1':
        reply = "回應給特定訊息1的回覆"
    elif msg == '特定訊息2':
        reply = "回應給特定訊息2的回覆"
    else:
        reply = "未知訊息"

    line_bot_api.reply_message(tk, TextSendMessage(text=reply))
    print(msg, tk)

def handle_postback(event):
    global ID
    postback_data = event.postback.data
    print("Postback data:", postback_data)
    # buttons_template = TemplateSendMessage(
    #     alt_text=restaurant["name"],
    # )


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handle_text_message(event)

@handler.add(PostbackEvent)
def handle_postback_event(event):
    handle_postback(event)

# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

# access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
# secret = 'e90e4acf2cce57e39e9c69032f23ea22'
