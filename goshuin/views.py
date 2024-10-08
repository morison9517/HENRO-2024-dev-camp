import math
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, LocationMessage, TextSendMessage
from .models import Temple
import logging
import csv
import os

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

logger = logging.getLogger(__name__)

def my_view(request):
    return HttpResponse('Hello, world', status=200)

@csrf_exempt
def line_callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    logger.info("Received body: %s", body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # 地球の半径 (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    logger.info("Location message received: %s", event.message)

    user_lat = event.message.latitude
    user_lon = event.message.longitude

    try:
        temples = Temple.objects.all()
        closest_temple = None
        closest_distance = float('inf')

    # データベースから寺院の情報を取得
    
        for temple in temples:
            distance = calculate_distance(user_lat, user_lon, temple.latitude, temple.longitude)
            if distance < closest_distance:
                closest_distance = distance
                closest_temple = temple

        if closest_temple and closest_distance < 1:  # 1.5km以内に近い寺院がある場合
            reply_message = f"{closest_temple.name}に近づいています！"
        else:
            reply_message = "近くに寺院はありません"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

        logger.info("Reply sent: %s", reply_message)

    except Exception as e:
        logger.error("Error processing location message: %s", str(e))


def callback(request):
    return HttpResponse('Callback view is working!')

#--------------------------------------------------------------------------
#番号に合わせて説明を返す


# CSVファイルからデータを読み込む関数
def get_response_from_csv(number):
    csv_path = os.path.join(os.path.dirname(__file__), 'explanation.csv')
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['number'] == str(number):
                return row['explanation']
    return "該当するデータがありません。"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_input = event.message.text

    if user_input.isdigit():
        explanation = get_response_from_csv(user_input)
    else:
        explanation = "数字を入力してください。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=explanation)
    )
