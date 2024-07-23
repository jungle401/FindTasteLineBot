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
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action={
                "type": "postback",
                "data": "action=show_menu1"
            }
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1251, y=0, width=1250, height=843),
            action={
                "type": "postback",
                "data": "action=show_menu2"
            }
        )
    ]
)

rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)

with open("r3.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)

