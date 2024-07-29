# Essential libraries
import random
import requests
import json
from flask import Flask, request

# Line message APIs
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, LocationAction, LocationMessage, CarouselTemplate
from linebot.models import * 
from linebot.v3.messaging import MessagingApi

# Google APIs
import googlemaps

# Configurations
app = Flask(__name__)
access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
secret = 'e90e4acf2cce57e39e9c69032f23ea22'
GOOGLE_API_KEY='AIzaSyBeYAAaSwCbvKcLBGinSfmApezIBOd1RK4'

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

# Global variables
lat = lng = address = ''
star = 3
menu_category = 0
menu_category_size = 2

# ---------------------------------------------------------------------------------------------------------
def handle_location_message(event):
    global lat, lng, address
    # 取得使用者分享的位置資訊
    lat = event.message.latitude
    lng = event.message.longitude
    address = event.message.address

    # 在這裡可以處理使用者分享位置資訊的相關邏輯，例如存入資料庫、進行位置相關的運算等
    reply = f"搜尋位置設定：{address}\n"
    reply += f"最低可接受評價：{star}\n"
    reply += "***  設定完成，請開始搜尋！***"

    # 回覆訊息給使用者
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

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

def get_location(event):
    location_action = LocationAction(label='分享我的位置',)
    tk = event.reply_token

    # 創建按鈕模板訊息
    buttons_template = ButtonsTemplate(
        title='請分享您的位置',
        text='請點擊下面的按鈕分享您的位置',
        actions=[location_action]
    )

    # 發送按鈕模板訊息給使用者
    template_message = TemplateSendMessage(
        alt_text='請分享您的位置',
        template=buttons_template
    )

    # 使用 LineBot API 回覆訊息給使用者
    line_bot_api.reply_message(tk, template_message)
    return

from rich_menus.rich_menu_modules import *

def handle_rich_menu_change(event):
    global star
    if event.postback.data[:4] == 'star':
        star = int(event.postback.data[4])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'可接受評價下限: {star}'))
    elif event.postback.data[:3] == 'cat':
        global menu_category
        if event.postback.data[4:] == 'add':
            menu_category = menu_category + 1 if menu_category != menu_category_size - 1 else menu_category
        elif event.postback.data[4:] == 'minus':
            menu_category = menu_category - 1 if menu_category != 0 else menu_category

    user_id = event.source.user_id

    line_bot_api.link_rich_menu_to_user(user_id, menu_id_map[(menu_category, star)])

def handle_postback(event):

    global lat, lng, address

    if event.postback.data in rich_menu_change_events:
        handle_rich_menu_change(event)
        return

    if event.postback.data == 'location':
        get_location(event)
        return

    if address == '':
        get_location(event)
        return
    target_type = event.postback.data

    addurl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY, address)
    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()

    foodStoreSearch = ""
    if target_type in {'restaurant', 'cafe', 'convenience_store'}:
        foodStoreSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type={}&language=zh-TW".format(GOOGLE_API_KEY, lat, lng, target_type)
    else:
        foodStoreSearch = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={}&query={}&language=zh-TW&location={},{}&radius=5000".format(GOOGLE_API_KEY, target_type, lat, lng)

    foodReq = requests.get(foodStoreSearch)
    nearby_restaurants_dict = foodReq.json()
    top20_restaurants = nearby_restaurants_dict["results"]
    res_num = (len(top20_restaurants))

    # Find targes rating larger than some point
    bravo=[]
    for i in range(res_num):
        try:
            if top20_restaurants[i]['rating'] >= star:
                bravo.append(i)
        except Exception as e:
            print(f"Caught low rating ones:{e}")
            KeyError

    if len (bravo) <= 0:
        reply = "這附近沒東西可以吃"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    if len(top20_restaurants) == 0:
        reply = "這附近沒有："
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    selected_restaurants = []
    random.shuffle(top20_restaurants)
    for restaurant in top20_restaurants:
        if restaurant.get("photos") is not None and len(restaurant['name']) < 40:
            selected_restaurants.append(restaurant)
            if len(selected_restaurants) == 10:
                break

    carousel_template = CarouselTemplate()
    for restaurant in selected_restaurants:
    # restaurant = top20_restaurants[random.choice(bravo)]
        if restaurant.get("photos") is None:
            thumbnail_image_url = None
        else:
            photo_reference = restaurant["photos"][0]["photo_reference"]
            photo_width = restaurant["photos"][0]["width"]
            thumbnail_image_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GOOGLE_API_KEY}&photoreference={photo_reference}&maxwidth={photo_width}"

        # Assemble reply message
        rating = "無" if restaurant.get ("rating") is None else restaurant[ "rating"]
        address="沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
        if address == "沒有資料":
            address = restaurant["formatted_address"]
        details = "Google Map評分:{}\n地址:{}".format(rating, address)
        # google map url for restaurants
        map_url = f"https://www.google.com/maps/search/?api=1&query={restaurant['geometry']['location']['lat']},{restaurant['geometry']['location']['lng']}&query_place_id={restaurant['place_id']}"

        column = CarouselColumn(
            thumbnail_image_url=thumbnail_image_url,
            title=restaurant['name'],
            text=details,
            actions=[
                URITemplateAction(
                    label='Open in google map',
                    uri=map_url
                )
            ]
        )
        carousel_template.columns.append(column)

    template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=carousel_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

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

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message_event(event):
    handle_location_message(event)

# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
