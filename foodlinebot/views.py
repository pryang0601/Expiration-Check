from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    StickerSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)
from foodlinebot.models import *

from datetime import datetime, timedelta
app = Flask(__name__)
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 

from django.http import JsonResponse
user_states = {}
user_food =[]
user_food_name =""
user_expiration_date =""
@csrf_exempt
#@app.route("/callback", methods=['POST'])
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                global user_food
                global user_states
                user_input = event.message.text
                user_id = event.source.user_id
                current_state = user_states.get(user_id, None)
                if user_input == '新增食物':
                    # Ask the user to type the food name
                    
                    user_food = []
                    user_states = {}
                    user_states[user_id] = 'waiting_for_food_name'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入食物名稱")
                    )
                elif current_state == 'waiting_for_food_name':
                    # Save the food name and ask for the expiration date
                    # global user_food
                    # global user_states
                    user_states[user_id] = 'waiting_for_expiration_date'
                    user_food.append(user_input)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入食物過期日期，請以-做區隔\n(例:2024-xx-xx)")
                    )
                elif current_state == 'waiting_for_expiration_date':
                    # Save the expiration date and reply with "done"
                    # global user_food
                    # global user_states
                    user_states.pop(user_id, None)
                    user_food.append(user_input)
                    sticker_message = StickerSendMessage(
                        package_id = '789',
                        sticker_id = '10866'
                    )
                    reply_arr = []
                    reply_arr.append(TextSendMessage(text="新增成功！"))
                    reply_arr.append(sticker_message)
                    
                    line_bot_api.reply_message(
                                event.reply_token,
                                reply_arr
                            )
                    
                    # Save the food information to the Django database
                    today = datetime.now().date()
                    user_food[1] = user_food[1].replace('/', '-').replace('.', '-')
                    user_food[1] = datetime.strptime(user_food[1], "%Y-%m-%d").date()
                    food = Food_Info(name=user_food[0], start= today, expiration=user_food[1])
                    food.save()
                    # Reset the session after completing the task
                elif user_input == '食物一覽表':
                    datas=Food_Info.objects.all().order_by('expiration')
                    if len(datas)>0:
                        message = ''
                        for idx,data in enumerate(datas):
                            message+= str(idx+1)+". "+data.name+"是在"+str(data.start)+"進來的，並會在"+str(data.expiration)+"過期。\n\n"
                            
                        message+="請享用並開始減肥！"
                        sticker_message = StickerSendMessage(
                            package_id = '6325',
                            sticker_id = '10979906'
                        )
                        reply_arr = []
                        reply_arr.append(TextSendMessage(text=message))
                        reply_arr.append(sticker_message)
                        
                        line_bot_api.reply_message(
                                    event.reply_token,
                                    reply_arr
                                )
                    else:
                        sticker_message = StickerSendMessage(
                            package_id = '446',
                            sticker_id = '2023'
                        )
                        reply_arr = []
                        reply_arr.append(TextSendMessage(text="家裡沒吃的"))
                        reply_arr.append(sticker_message)
                        
                        line_bot_api.reply_message(
                                    event.reply_token,
                                    reply_arr
                                )
                elif user_input =='刪除食物':
                    user_states[user_id] = 'waiting_for_food_name_to_delete'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="請輸入食物名稱")
                    )
                elif current_state == 'waiting_for_food_name_to_delete':
                    user_states.pop(user_id, None)
                    data=Food_Info.objects.filter(name=user_input)
                    data.delete()
                    sticker_message = StickerSendMessage(
                        package_id = '446',
                        sticker_id = '1999'
                    )
                    reply_arr = []
                    reply_arr.append(TextSendMessage(text="刪除成功"))
                    reply_arr.append(sticker_message)
                    line_bot_api.reply_message(
                        event.reply_token,
                        reply_arr
                    )
                elif user_input == '需要緊急處理的食物':
                    reply_arr = []
                    today = datetime.now().date()
                    danger_foods = Food_Info.objects.filter(expiration__lt=today + timedelta(days=7)).values_list('name', 'expiration')
                    message = ''
                    if len(danger_foods)>0:
                        for idx,danger_food in enumerate(danger_foods):
                            days_left = (danger_food[1].date() - today).days
                            if days_left > 0:
                                message+= str(idx+1)+". "+danger_food[0]+"會在"+str(danger_food[1])+"過期，還剩"+str(days_left)+"天。\n\n"
                            else:
                                message+= str(idx+1)+". "+danger_food[0]+"已經在"+str(danger_food[1])+"過期了，過期"+str(abs(days_left))+"天。\n\n"
                            
                        message+="請儘速吃完並開始減肥！"
                        reply_arr.append(TextSendMessage(text=message))
                        sticker_message = StickerSendMessage(
                            package_id = '1070',
                            sticker_id = '17867'
                        )
                        reply_arr.append(sticker_message)
                    else:
                        sticker_message = StickerSendMessage(
                        package_id = '6325',
                        sticker_id = '10979926'
                        )
                        reply_arr.append(TextSendMessage(text="沒有要過期的食物。"))
                        reply_arr.append(sticker_message)
                        
                    line_bot_api.reply_message(
                                event.reply_token,
                                reply_arr
                            )
                else:
                    sticker_message = StickerSendMessage(
                            package_id = '6325',
                            sticker_id = '10979923'
                    )
                    line_bot_api.reply_message(
                                event.reply_token,
                                sticker_message
                            )
        return HttpResponse()
    
    else:
        return HttpResponseBadRequest()