import requests

headers = {'Authorization':'4F6X3x4rRWsG3Chx/eLjE45/Kg8inU6Cs9pUo/2riYChvde4wT3XVs/qPZjOUe7GHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZPnMdESforLlF+y/6maewyfXOIV9IHNts9nVY+qSOVRLQdB04t89/1O/w1cDnyilFU='}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-fe347e02fb95ac615c2449ca5b653dfc', headers=headers)

print(req.text)
