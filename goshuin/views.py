from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, LocationMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
from .models import Temple

line_bot_api = LineBotApi('YOUR_LINE_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_LINE_CHANNEL_SECRET')

def haversine(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    R = 6371.0  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c

def get_nearest_temple(user_lat, user_lon):
    nearest_temple = None
    min_distance = float('inf')
    
    for temple in Temple.objects.all():
        distance = haversine(user_lat, user_lon, temple.latitude, temple.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_temple = temple
    
    return nearest_temple, min_distance

@csrf_exempt
def callback(request):
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
    user_lon = event.message.longitude
    nearest_temple, distance = get_nearest_temple(user_lat, user_lon)

    if distance <= 0.2:  # 200m以内を近づいたと定義
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{nearest_temple.name}に近づきました！")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="あなたは目的地の近くにはいません。")
        )

@handler.add(MessageEvent)
def handle_message(event):
    if event.message.text == "位置情報を送信してください":
        buttons_template = ButtonsTemplate(
            title='位置情報の共有',
            text='位置情報を送信するには、以下のボタンをタップしてください。',
            actions=[
                MessageAction(label='位置情報を送信', text='位置情報を送信してください')
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='位置情報の共有',
            template=buttons_template
        )
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )

