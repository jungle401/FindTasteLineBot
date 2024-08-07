# Find Taste Line Bot

# Table of Contents
- [Example](#Example)
- [QR code](#QR_Code)
- [Usage](#Usage)

---
A line bot provide fast search for restaurants or like using google map API.

---
## Tutorial
You may refer to the [development process](https://dog-hip-46a.notion.site/LineBot-TasteAdvisor-f55c6072cbb942469e61fa34725542d0#fcff606b8dd74860860106ce4faf4f32)

---
## Example
![screen shots](images/demo.png)

---


## QR_Code
Scan the QR code below to use this service, but please note that it may cease to operate at some point.
<img src="images/qr_code.png" alt="qr_code" width="200">

---
Alternatively, you can set up your own instance based on the repository.

---

## Usage
Issue the following tokens on LINE Message API and Google Map API, and configure them within `ga.py`.

```=python3
# Configurations
access_token = 'DDOS1nJL2oxe7nmekZ0OhZTFSIG0RbR9RdOnM9wJnGBfQlrmvndAMt5khcI+0aTOHTh4iepuG0LPTTEhfWyChjUtmy/ARuqC5ga9DcD0LZOYrxmrmGYooplhWRWjOeB+k0ikq6gy0fBGPEr9rkCVCwdB04t89/1O/w1cDnyilFU='
secret = 'e90e4acf2cce57e39e9c69032f23ea22'
GOOGLE_API_KEY='AIzaSyBeYAAaSwCbvKcLBGinSfmApezIBOd1RK4'
```

The process runs on port 300 by default.
```
# tty1
ngrok http 3000
# tty2
python3 ga.py
```

