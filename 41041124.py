from distutils.log import debug
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('XXX')
handler = WebhookHandler('XXX')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input=event.message.text
    reply=[]
    Total=[]
    s=list(input)
    for i in range(0,len(input)):
        Total.append(int(s[i]))
    reply.append(TextSendMessage(text="您輸入:"+input))
    reply.append(TextSendMessage(text=f"全部總和為:{sum(Total)}"))

    line_bot_api.reply_message(
        event.reply_token,
        reply)
#event.message.text是你輸入的內容

if __name__ == "__main__":
    app.run(debug=True)