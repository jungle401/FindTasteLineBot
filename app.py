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
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import * 

from linebot.v3.messaging import MessagingApi


# ---------------------------------------------------------------------------------------------------------
app = Flask(__name__)

access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
secret = 'e90e4acf2cce57e39e9c69032f23ea22'
line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
handler = WebhookHandler(secret)                     # 確認 secret 是否正確

@app.route("/", methods=['POST', 'GET'])
def linebot2():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type=='text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            # print(json.dumps(json_data, indent=4))
            reply = msg
        else:
            reply = '你傳的不是文字呦～'
        # print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))# 回傳訊息
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
# ---------------------------------------------------------------------------------------------------------

# access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
# secret = 'e90e4acf2cce57e39e9c69032f23ea22'
