import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,ImageMessage, TextSendMessage, FollowEvent
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
@handler.add(MessageEvent, message=TextMessage) #引数に処理したいイベントを指定してください
def handle_message(event):
    text = event.message.text
    if text == 'おはよう':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='おはようございます!'))
    elif text == 'こんにちは':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='こんにちは！'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

@handler.add(MessageEvent, message=ImageMessage)#引数に処理したいイベントを指定してください
def handle_message(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='画像を受信しました'))


# フォローイベント時の処理
@handler.add(FollowEvent)
def handle_follow(event):
    # 誰が追加したかわかるように機能追加
    profile = line_bot_api.get_profile(event.source.user_id)  # 取得したプロフィールをprofileに格納しています
    line_bot_api.push_message(Uad6b2718be2fa3e98ecdd9e783aa83c8,
                              TextSendMessage(text="表示名:{}\ユーザID:{}\n画像のURL:{}\nステータスメッセージ:{}" \
                                              .format(profile.display_name, profile.user_id, profile.picture_url,
                                                      profile.status_message)))

    # 友達追加したユーザにメッセージを送信
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='友達追加ありがとうございます'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)