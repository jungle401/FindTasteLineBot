from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
from linebot.models import * 

import googlemaps

import requests
import json

from time import sleep

gmaps = googlemaps.Client(key='AIzaSyAwSqXZAT-hbLYyee1ovzAyo6ybIX0OVag')
id_arr = []
where = ""
condition = ""
ID = ""
count = 0

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('qoyD2zNX5UYze2bNAUw8CWjG3khKFEXXukH1j/NeY2n2Y3RhvmLl5P7EqdN4RgkY02zM5GrujcflkE6esYaRowPIMcAELyH7mmOkRoYXdoQguDBkx2VhTDIzKpxGdoMfKrf6JLVD6LanueKK0hD/FgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bbaadb5d63659589e204986ce63a89f8')

headers = {"Authorization":"Bearer qoyD2zNX5UYze2bNAUw8CWjG3khKFEXXukH1j/NeY2n2Y3RhvmLl5P7EqdN4RgkY02zM5GrujcflkE6esYaRowPIMcAELyH7mmOkRoYXdoQguDBkx2VhTDIzKpxGdoMfKrf6JLVD6LanueKK0hD/FgdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}
'''
body = {
    "size": {"width": 2500, "height": 843},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "點我開始找地方",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 100, "height": 843},
          "action": {"type": "postback", "data": "back"}
        },
        {
          "bounds": {"x": 100, "y": 0, "width": 800, "height": 843},
          "action": {"type": "postback", "data": "火鍋"}
        },
        {
          "bounds": {"x": 900, "y": 0, "width": 800, "height": 843},
          "action": {"type": "postback", "data": "麵食"}
        },
        {
          "bounds": {"x": 1700, "y": 0, "width": 800, "height": 843},
          "action": {"type": "postback", "data": "便當"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)
'''
'''
rich_menu_list = line_bot_api.get_rich_menu_list()

for rich_menu in rich_menu_list:
    line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)
'''

'''
with open("menu2.png", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-e5bacd478acab1928620a759862d8de0", "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-f60fdf1ae4acfb2a3633e8a13379b8ea', 
                       headers=headers)
print(req.text)
'''

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


def reply_ten_location(replytoken, page_number):
    carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[]
            )
        )
    global id_arr
    global count
    global ID

    if page_number>5:
        page_number = 5
    for i in range(10*page_number, 10*(page_number+1)):
        details = gmaps.place(place_id=id_arr[i],language='zh-TW')
        result = details.get('result') 
        name = result.get('name')
        address = result.get('formatted_address')
        phone = result.get('formatted_phone_number')
        rating = result.get('rating')
        if phone == None:
            phone = '無'
        photos = result.get('photos')
        photo_reference = ''
        try:
            photo_reference = photos[1].get('photo_reference')
        except TypeError:
            photo_reference = ''
        except IndexError:
            print("IndexError")
        carousel_template_message.template.columns.append(
            CarouselColumn(
                thumbnail_image_url='https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+photo_reference+'&key=AIzaSyAwSqXZAT-hbLYyee1ovzAyo6ybIX0OVag',
                title=name,
                text='電話:'+phone+"\n"+'評價:'+str(rating),
                actions=[
                    MessageAction(label='#'+str(i+1)+'商家照片', text='#'+str(i+1)+'商家照片'),
                    MessageAction(label='#'+str(i+1)+'商家地圖', text='#'+str(i+1)+'商家地圖'),
                    MessageAction(label='#'+str(i+1)+'營業時間', text='#'+str(i+1)+'營業時間')
                ]
            )
        )
    line_bot_api.reply_message(replytoken, carousel_template_message)

    count=count+1

    if count == 6:
        line_bot_api.push_message(ID,[TextSendMessage(text='沒有店家了!'),])
    else:
        line_bot_api.push_message(ID, 
            [TextSendMessage(
                text='下一頁還有其他店家哦!',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            image_url="https://image.flaticon.com/icons/png/512/128/128574.png",
                            action=PostbackAction(label="下一頁", data="下一頁")
                        ),
                    ])),])

#處理postback
@handler.add(PostbackEvent)
def handle_postback(event):
    global where
    global condition
    global ID
    global place_api
    global query_text
    place_api = 0
    data = event.postback.data
    try:
        if data == '餐廳' or data == '咖啡廳' or data=='超商':
            if data == '餐廳':
                where = "restaurant"
            if data == '咖啡廳':
                where = "cafe"
            if data =='超商':
                where = "convenience_store"
            line_bot_api.push_message(ID,[TextSendMessage(text='你選了「'+data+'」!'),])
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請選擇條件',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            image_url="https://image.flaticon.com/icons/png/512/55/55182.png",
                            action=PostbackAction(label="距離", data="距離")
                        ),
                        QuickReplyButton(
                            image_url="https://image.flaticon.com/icons/png/512/66/66027.png",
                            action=PostbackAction(label="評價", data="評價")
                        ),
                    ])))

        elif data == '火鍋' or data == '麵食' or data == '便當':
            line_bot_api.push_message(ID,[TextSendMessage(text='你選了「'+data+'」!'),])
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='丟出想查詢的位置吧!',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            image_url="https://image.flaticon.com/icons/png/512/44/44334.png",
                            action=LocationAction(label="送出位置")
                        ),
                    ])))
            place_api = 1
            query_text = event.postback.data

        elif data == '距離' or data=='評價':
            if data == '距離':
                condition = "distance"
            elif data == '評價':
                condition = "rating"
            line_bot_api.push_message(ID,[TextSendMessage(text='你選了「'+data+'」!'),])
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='丟出想查詢的位置吧!',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            image_url="https://image.flaticon.com/icons/png/512/44/44334.png",
                            action=LocationAction(label="送出位置")
                        ),
                    ])))
        elif data == '下一頁':
            global page_num
            page_num = page_num + 1
            reply_ten_location(event.reply_token, page_num)
        elif data == 'next':     #menu按下一頁
            line_bot_api.link_rich_menu_to_user(ID, "richmenu-e5bacd478acab1928620a759862d8de0")
        elif data == 'back':     #menu按上一頁
            line_bot_api.link_rich_menu_to_user(ID, "richmenu-f60fdf1ae4acfb2a3633e8a13379b8ea")

    except LineBotApiError:
        message = TextSendMessage(text="詢問前打招呼是基本的禮儀哦!")
        line_bot_api.reply_message(event.reply_token, message)  

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global ID
    ID = event.source.user_id

    print(type(event.message.text))
    global id_arr
    if event.message.text[0]=='#':
        if event.message.text[4]=='照' or event.message.text[5]=='照': #商家照片
            if event.message.text[2]=='商':  #如果是個位數的#num店家
                placeid = id_arr[int(event.message.text[1])-1]
            else:                            #如果是兩位數的#num店家
                placeid = id_arr[int(event.message.text[1])*10+int(event.message.text[2])-1]
            details = gmaps.place(place_id=placeid,language='zh-TW')
            result = details.get('result') 
            photos = result.get('photos')
            image_urls = []
            try: 
                for photo in photos:
                    photo_reference = photo.get('photo_reference')
                    googleImageUrl = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference='+photo_reference+'&key=AIzaSyAwSqXZAT-hbLYyee1ovzAyo6ybIX0OVag'
                    image_urls.append(googleImageUrl)
                image_carousel_template_message = TemplateSendMessage(
                    alt_text='ImageCarousel template',
                    template=ImageCarouselTemplate(
                        columns=[]
                    )
                )
                for image_url in image_urls:
                    image_carousel_template_message.template.columns.append(
                        ImageCarouselColumn(
                            image_url=image_url,
                            action=PostbackAction(
                                label='商家圖片',
                                data='picture'
                            )
                        )
                    )
                line_bot_api.reply_message(event.reply_token, image_carousel_template_message)
            except TypeError:
                message = TextSendMessage(text="No image available")
                line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text[4]=='地' or event.message.text[5]=='地': #商家地圖
            if event.message.text[2]=='商':  #如果是個位數的#num店家
                placeid = id_arr[int(event.message.text[1])-1]
            else:                            #如果是兩位數的#num店家
                placeid = id_arr[int(event.message.text[1])*10+int(event.message.text[2])-1]
            details = gmaps.place(place_id=placeid,language='zh-TW')
            result = details.get('result') 
            name = result.get('name')
            address = result.get('formatted_address')
            geometry = result.get('geometry')
            location = geometry.get('location')
            latitude = location.get('lat')
            longitude = location.get('lng')
            try:
                line_bot_api.reply_message(
                        event.reply_token,
                        LocationSendMessage(
                            title=name, address=address,
                            latitude=latitude, longitude=longitude
                        )
                    )
            except AttributeError:
                message = TextSendMessage(text="No map available")
                line_bot_api.reply_message(event.reply_token, message)    
        elif event.message.text[2]=='營' or event.message.text[3]=='營': #營業時間
            if event.message.text[2]=='營':  #如果是個位數的#num店家
                placeid = id_arr[int(event.message.text[1])-1]
            else:                            #如果是兩位數的#num店家
                placeid = id_arr[int(event.message.text[1])*10+int(event.message.text[2])-1]
            details = gmaps.place(place_id=placeid,language='zh-TW')
            result = details.get('result') 
            try:
                opening_hours = result.get('opening_hours')
                weekday_text = opening_hours.get('weekday_text')
                
                bubble = BubbleContainer(
                    direction='ltr',
                    body=BoxComponent(
                        layout='vertical',
                        align= 'center',
                        contents=[
                            # info
                            BoxComponent(
                                layout='vertical',
                                contents=[
                                    BoxComponent(
                                        layout='vertical',
                                        contents=[
                                            TextComponent(text=weekday_text[0], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[1], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[2], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[3], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[4], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[5], wrap=True, size='md', flex=0),
                                            TextComponent(text=weekday_text[6], wrap=True, size='md', flex=0)
                                        ]
                                    ),
                                ],
                            )
                        ],
                    ),
                )
                message = FlexSendMessage(alt_text="營業時間", contents=bubble)
                line_bot_api.reply_message(event.reply_token, message)
            except AttributeError:
                message = TextSendMessage(text="No opening hours available")
                line_bot_api.reply_message(event.reply_token, message)  

        message = FlexSendMessage(alt_text="清單", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "嗨":
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

#處理位置訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    global condition
    global where
    global count
    global place_api
    global query_text
    count = 0
    if place_api==0:
        if condition == "distance":
            result = gmaps.places_nearby(
                location={"lat" : event.message.latitude, "lng" : event.message.longitude},
                rank_by='distance',
                type=where,
                language='zh-TW'
            )
        elif condition == "rating":
            result = gmaps.places_nearby(
                location={"lat" : event.message.latitude, "lng" : event.message.longitude},
                radius=1000,
                rank_by='prominence',
                type=where,
                language='zh-TW'
            )
    if place_api==1:
        result = gmaps.places(
            query=query_text,
            location={"lat":event.message.latitude,"lng":event.message.longitude}
        )
    result_arr = result.get('results') #.get()用在取得dict的attribute; result_arr是搜尋出來的店家陣列
    global id_arr
    del id_arr[:]
    for results in result_arr:
        print(results)
        id_arr.append(results.get('place_id'))
    token = result.get('next_page_token')
    
    global page_num
    page_num = 0
    reply_ten_location(event.reply_token, page_num) #第一次回傳10間店家

    sleep(2)
    if place_api==0:
        result = gmaps.places_nearby(
                page_token=token    #參數直接放token就好 會依照同一個地點的搜尋方式套用在此
            )
    elif place_api==1:
        result = gmaps.places(
            page_token=token,    #參數直接放token就好 會依照同一個地點的搜尋方式套用在此
            query=query_text
        )
    del result_arr[:] 
    result_arr = result.get('results')
    for results in result_arr:
        id_arr.append(results.get('place_id'))
    token = result.get('next_page_token')
    sleep(2)
    if place_api==0:
        result = gmaps.places_nearby(
                page_token=token    #參數直接放token就好 會依照同一個地點的搜尋方式套用在此
            )
    elif place_api==1:
        result = gmaps.places(
            page_token=token,    #參數直接放token就好 會依照同一個地點的搜尋方式套用在此
            query=query_text
        )
    del result_arr[:] 
    result_arr = result.get('results')
    for results in result_arr:
        id_arr.append(results.get('place_id'))
    place_api = 0

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
