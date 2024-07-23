import requests
import random
import json
GOOGLE_API_KEY='AIzaSyBeYAAaSwCbvKcLBGinSfmApezIBOd1RK4'

# if linevessage [e:3]=="隨便吃"：
#     address = ""
#     lineMes = lineMessage
#     if lineMes [4: -1] ==""
address = "苗栗市玉清路"
# else:
# address = lineMes [4: -1]
addurl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY, address)
addressReq = requests.get(addurl)
addressDoc = addressReq.json ( )
lat = addressDoc['results'][0]['geometry']['location']['lat']
lng = addressDoc['results'][0]['geometry']['location']['lng']

foodStoreSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(GOOGLE_API_KEY, lat, lng)
foodReq = requests.get(foodStoreSearch)
nearby_restaurants_dict = foodReq.json ()
# print(json.dumps(nearby_restaurants_dict, indent=4))
top20_restaurants = nearby_restaurants_dict["results"]
print(json.dumps(top20_restaurants, indent=4))
res_num = (len(top20_restaurants))
#  取得評分高於3.9的店家位置
bravo=[]
for i in range(res_num):
    try:
        if top20_restaurants[i]['rating'] > 3.9:
            print ('rate: ', top20_restaurants[i]['rating'])
            print ('rate: ', top20_restaurants[i]['place_id'])
            bravo.append(i)
    except Exception as e:
        print(f"Caught unexpected error:{e}")
        KeyError
if len (bravo) < 0:
    content = "沒東西可以吃"
# restaurant = random.choice(top26_restaurants)沒有的話隨便選一間
# 從高於3.9的店家隨機選一間
restaurant = top20_restaurants[random.choice(bravo)]
# 檢査餐廳有沒有照片，有的話會顯示
if restaurant. get ("photos ") is None:
    thumbnail_image_url = None
else:
#  根據文件，最多只會有一張照片
    photo_reference = restaurant ["photos "][0]["photo_reference"]
    photo_width = restaurant ["photos"][0]["width"]
    thumbnail_image_ur = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format (GOOGLE_API_KEY, photo_reference, photo_width)
# 組裝餐廳詳細資訊
rating = "無" if restaurant.get ("rating") is None else restaurant[ "rating"]
address="沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
details = "Google Map評分:{}\n地址:{}".format(rating, address)
# print (details)
# 取得餐廳的 Google map 網址
map_url = "https://www.google.com/maps/search/?api-1&query={lat}, {long}&query_place_id={place_id}".format(lat=restaurant["geometry"]["location"]["lat"], long=restaurant["geometry"]["location"]["lng"],place_id=restaurant["place_id"])
