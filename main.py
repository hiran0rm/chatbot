import os
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

line_bot_api = LineBotApi('85GuDL0mm/fktE/4QksofPV5VrmZQVbS2/VhT+F1wiu356SJk/lLyXUN+F4vqEr8Dd60RnjR32/7sQ0vcPvOrXUMUpoegYOXR6S04McNNJ1cn1CwwZyc7aHkC396KD+iszTsSPN5yKUXu752goSzGwdB04t89/1O/w1cDnyilFU=') #アクセストークンを入れてください
handler = WebhookHandler('d9040f4fffb01b6c55812dc39bbdcd69') #Channel Secretを入れてください


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#テキストメッセージが送信されたときの処理
@handler.add(MassageEvent, message=TextMessage) #引数に処理したいイベントを指定してください
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='メッセージを受信しました')) #送りたいメッセージを入れてください


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)