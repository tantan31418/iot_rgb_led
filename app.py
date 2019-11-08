from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from tan_token import *
from initsetup import *

import json
import requests


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

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

# pin_num=5
# on_off=0
# color="\color/"

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text[0]=='R':
        color = 'RED'
        pin_num=12
        if event.message.text[1] == '1':
            on_off=1
    elif event.message.text[0]=='B':
        pin_num=13
        if event.message.text[1] == '1':
            on_off=1
    elif event.message.text[0]=='G':
        pin_num=5
        if event.message.text[1] == '1':
            on_off=1
    else :
        donthavepinflag=1
        pin_num=5
        on_off=1
        requests.get('https://cloud.arest.io/{dorm}/digital/5/0')
        requests.get('https://cloud.arest.io/{dorm}/digital/12/0')
        requests.get('https://cloud.arest.io/{dorm}/digital/13/0')
    r = requests.get('https://cloud.arest.io/{dorm}/digital/{pin}/{turn}'.format(dorm=dorm_id,pin=pin_num,turn=on_off))
    data = json.loads(r.content)
    def send_message_content(col,onoff):
        if onoff:
            turned='on'
        else:
            turned='off'
        return "{coll} has been turned {turn}".format(coll=col,turn=turned)

    mess_to_send = "{col} has been turned {turn}".format(color,on_off)
    if donthavepinflag==1:
        message=TextSendMessage(text="There is no such Color,ERROR!")
    else:
        if data["connected"]:
            message = TextSendMessage(text=send_message_content(color,on_off))
        else :
            message = TextSendMessage(text="Board is not online, please try again later")
    line_bot_api.reply_message(event.reply_token, message)

#if input==blue: pin_num=13
#if input==red: pin_num=12
#if input==green: pin_num=5
# if event.message.text[1] = '1': on_off=1

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
