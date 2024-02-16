import json
from _decimal import Decimal

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myauthentication.models import CustomUser as User
from utilities.send_sms import send_sms_message

from .serializers import *
from userprofile.models import UserProfile

url = "https://swahiliesapi.invict.site/Api"


@csrf_exempt
def is_monetization_on(request):
    monetization_on = MonetizationOn.objects.filter(monetization_on=True).exists()
    if monetization_on:
        return JsonResponse({'status': 'success', 'message': 'Monetization is On', 'status_code': 200})
    else:
        return JsonResponse({'status': 'error', 'message': 'Monetization is off', 'status_code': 400})


@csrf_exempt
def webhook_payment_endpoint(request):
    # Read the raw request body
    request_body = request.body
    data = json.loads(request_body)
    print(f'WEBHOOK PAYMENT: {data}')
    order_id = data['transaction_details']['order_id']
    user_id = data['transaction_details']['metadata']['user_id']
    purchase_order = Purchase.objects.get(id=order_id)
    user = User.objects.get(id=user_id)

    user.credits = user.credits - 200
    user.save()
    purchase_order.is_success = True
    purchase_order.save()

    return JsonResponse({'status': 'Successfully paid', 'data': data}, )


def make_payment(order_id, amount, phone_number, story_type, story_id, user_id):
    payload = json.dumps({
        "api": 170,
        "code": 104,
        "data": {
            "api_key": "NjIwYTI1NzY2MWVjNDBmYWFlZWIwNTA3NGVmNGMyNjg=",
            "order_id": order_id,
            "amount": amount,
            "username": "Kijiweni",
            "metadata": {
                "type": story_type,
                "story_id": story_id,
                "user_id": user_id,
                "story_type": story_type
            },
            "is_live": True,
            "phone_number": phone_number,

            "webhook_url": "https://kungwi.fxlogapp.com/api/webhook_payment_endpoint/"

        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


@csrf_exempt
def create_purchase_order(request):
    user_id = request.POST.get('user_id')
    story_type = request.POST.get('story_type')  # 'Audio' or 'Article'
    story_id = request.POST.get('story_id')
    amount = request.POST.get('amount')
    phone_number = request.POST.get('phone_number')
    user = User.objects.get(id=user_id)
    new_purchase = Purchase(user=user, story_type=story_type, story_id=story_id, amount_paid=amount)
    new_purchase.save()

    make_payment_response = make_payment(new_purchase.id, amount, phone_number, story_type, story_id, user_id)

    parsed_json = json.loads(make_payment_response)
    status_code = parsed_json['code']

    if status_code == 200:
        return JsonResponse({'status': 'success', 'message': 'Payment order created successfully', 'status_code': 200})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to create payment order', 'status_code': 400}),


@csrf_exempt
def webhook_buy_credit_endpoint(request):
    # Read the raw request body
    request_body = request.body
    data = json.loads(request_body)
    print(f'WEBHOOK PAYMENT: {data}')
    order_id = data['transaction_details']['order_id']
    amount_paid = data['transaction_details']['amount']
    user_id = data['transaction_details']['metadata']['user_id']
    phone_number = data['transaction_details']['metadata']['phone_number']
    credit_amount = data['transaction_details']['metadata']['credit_amount']
    purchase_order = BuyCredits.objects.get(id=order_id)

    user = User.objects.get(id=user_id)

    if amount_paid >= 1000:
        purchase_order.is_success = True
        user.credits = user.credits + int(credit_amount)
        user.save()
        purchase_order.save()

    # send sms notification to admin
    try:
        numbers = ['255629598762', '255755817871']
        message = f'Habari Kijiweni, {user.username} mwenye namba {user.phone_number} amenunua TOKEN {credit_amount} kwa  Tzs {amount_paid}.'
        for number in numbers:
            send_sms_message(number, message)

        user_message = f'Hongera {user.username}, umefanikiwa kufanya manunuzi ya TOKEN {credit_amount} kwa  Tzs {amount_paid}. Unaweza kutumia TOKEN hizo kupakua story uipendayo.'
        send_sms_message(phone_number, user_message)
    except:
        pass

    return JsonResponse({'status': 'Successfully paid', 'data': data}, )


def buy_credit_make_payment(order_id, amount, phone_number, user_id, credit_amount):
    payload = json.dumps({
        "api": 170,
        "code": 104,
        "data": {
            "api_key": "NjIwYTI1NzY2MWVjNDBmYWFlZWIwNTA3NGVmNGMyNjg=",
            "order_id": order_id,
            "amount": amount,
            "username": "Kijiweni",
            "metadata": {
                "user_id": user_id,
                "credit_amount": credit_amount,
                "phone_number": phone_number
            },
            "is_live": True,
            "phone_number": phone_number,

            "webhook_url": "https://kungwi.fxlogapp.com/api/webhook_buy_credit_endpoint/"

        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text


@csrf_exempt
def create_buy_credit_order(request):
    user_id = request.POST.get('user_id')
    amount = request.POST.get('amount')
    credit_amount = request.POST.get('credit_amount')
    user = User.objects.get(id=user_id)
    phone_number = request.POST.get('phone_number')
    new_purchase = BuyCredits(user=user, amount_paid=amount)
    new_purchase.save()
    make_payment_response = buy_credit_make_payment(new_purchase.id, int(float(amount)), phone_number, user_id, credit_amount)

    parsed_json = json.loads(make_payment_response)
    status_code = parsed_json['code']

    if status_code == 200:
        return JsonResponse({'status': 'success', 'message': 'Payment order created successfully', 'status_code': 200})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to create payment order', 'status_code': 400}),


@csrf_exempt
def fetch_vifurushi(request):
    vifurushi = Vifurushi.objects.all()
    vifurushi_serializer = VifurushiSerializer(vifurushi,many=True).data
    return JsonResponse({'status': 'success', 'message': 'Vifurushi fetched successfully', 'status_code': 200,
                         'data': list(vifurushi_serializer)})


@csrf_exempt
def buy_story(request):
    try:

        story_type = request.POST.get('story_type')
        user_id = request.POST.get('user_id')
        story_id = request.POST.get('story_id')
        amount = request.POST.get('amount')
        token = request.POST.get('token')
        user = User.objects.get(id=user_id)
        purchase_order = Purchase.objects.create(user=user, story_type=story_type, story_id=story_id, amount_paid=amount)
        user = User.objects.get(id=user_id)

        user.credits = user.credits - int(token)
        user.save()
        purchase_order.is_success = True
        purchase_order.save()
        return JsonResponse({'status': 'Success', 'message': 'Umefanikiwa kununua STORY hii.', 'status_code': 200
                             } )
    except:
        return JsonResponse({'status': 'Error', 'message': 'Tatizo kununua STORY hii.Tafadhali wasiliana nasi WHATSAPP tukusaidie.', 'status_code': 400
                             })