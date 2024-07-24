from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds

# 設置 LINE 的 Channel Access Token
line_bot_api = LineBotApi('DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU=')
user_id = 'U39c4974696fe52a49832f713a9cbd648'

# 定義 Rich Menu 的尺寸
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="Nice Richmenu",
    chat_bar_text="Tap here",
    areas=[
        # Location
        RichMenuArea(
            bounds=RichMenuBounds(x=408, y=0, width=398, height=200),
            action={
                "type": "postback",
                "data": "location"
            }
        ),
        # star 1
        RichMenuArea(
            bounds=RichMenuBounds(x=979, y=0, width=233, height=200),
            action={
                "type": "postback",
                "data": "star1"
            }
        ),
        # star 2
        RichMenuArea(
            bounds=RichMenuBounds(x=1256, y=0, width=233, height=200),
            action={
                "type": "postback",
                "data": "star2"
            }
        ),
        # star 3
        RichMenuArea(
            bounds=RichMenuBounds(x=1539, y=0, width=233, height=200),
            action={
                "type": "postback",
                "data": "star3"
            }
        ),
        # star 4
        RichMenuArea(
            bounds=RichMenuBounds(x=1816, y=0, width=233, height=200),
            action={
                "type": "postback",
                "data": "star4"
            }
        ),
        # star 5
        RichMenuArea(
            bounds=RichMenuBounds(x=2099, y=0, width=233, height=200),
            action={
                "type": "postback",
                "data": "star5"
            }
        ),
        # cat_minus
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=200, width=194, height=643),
            action={
                "type": "postback",
                "data": "cat_minus"
            }
        ),
        # hot pot
        RichMenuArea(
            bounds=RichMenuBounds(x=194, y=200, width=711, height=643),
            action={
                "type": "postback",
                "data": "火鍋"
            }
        ),
        # 麵食
        RichMenuArea(
            bounds=RichMenuBounds(x=905, y=200, width=708, height=643),
            action={
                "type": "postback",
                "data": "麵食"
            }
        ),
        # 便當
        RichMenuArea(
            bounds=RichMenuBounds(x=1613, y=200, width=705, height=643),
            action={
                "type": "postback",
                "data": "便當"
            }
        ),
        # cat_add
        RichMenuArea(
            bounds=RichMenuBounds(x=2318, y=200, width=182, height=643),
            action={
                "type": "postback",
                "data": "cat_add"
            }
        ),
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print()
print(rich_menu_id)
print()

# with open("./rich_menus/sz2400x843/rm3.png", 'rb') as f:
with open("./rich_menus/images/sz2400x843/c2s5.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

