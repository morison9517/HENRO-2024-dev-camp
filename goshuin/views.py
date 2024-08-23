from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, LocationMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction
import math
from .models import Temple
from django.shortcuts import render

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def line_callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    user_lat = event.message.latitude
    user_lng = event.message.longitude

    def calculate_distance(lat1, lng1, lat2, lng2):
        R = 6371  # 地球の半径 (km)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat/2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    nearby_temple = None
    for temple in Temple.objects.all():
        distance = calculate_distance(user_lat, user_lng, temple.latitude, temple.longitude)
        if distance < 0.5:  # 0.5km以内なら通知
            nearby_temple = temple
            break

    if nearby_temple:
        reply_message = f"あなたは{nearby_temple.name}に近づいています！"
    else:
        reply_message = "近くに寺院はありません。"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

@handler.add(MessageEvent, message=TextSendMessage)
def handle_text_message(event):
    if event.message.text.lower() == '位置情報を送信する':
        buttons_template = ButtonsTemplate(
            title='位置情報送信',
            text='位置情報を送信するには、下のボタンをタップしてください。',
            actions=[
                PostbackAction(
                    label='位置情報を送信',
                    data='send_location'
                )
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='位置情報を送信するボタン',
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

def callback(request):
    return HttpResponse('Callback view is working!')


