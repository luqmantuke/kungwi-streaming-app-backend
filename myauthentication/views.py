import math
from random import random

from myauthentication.models import CustomUser
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.core.mail import send_mail, BadHeaderError
from .models import CustomUser as User
from kungwi import settings
from utilities.send_sms import send_sms_message
from .models import OTP
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from utilities.generate_otp import generateOTP


def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret


# Sign up user
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(phone_number=request.POST.get('phone_number')).first():
            return JsonResponse({'status': 'error', 'message': "This number already exists", 'status_code': 400},
                                status=400)
        if CustomUser.objects.filter(username=request.POST.get('username')).first():
            return JsonResponse({'status': 'error', 'message': "This username already exists", 'status_code': 400},
                                status=400)

        try:
            user = CustomUser.objects.create_user(request.POST.get('username'), password=request.POST.get('password'),

                                                  phone_number=request.POST.get('phone_number'),
                                                  )
            current_user = CustomUser.objects.get(username=request.POST.get('username'))
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'status': 'success', 'message': 'User created successfully', 'token': str(token),
                                 'username': str(current_user.username), 'user_id': str(current_user.id),
                                 'status_code': 201}, status=201)
        except:
            return JsonResponse({'status': 'error', 'message': 'User created successfully', 'status_code': 400}, status=400)
    else:
        print("I think it might not be post")
        return JsonResponse({'status': 'not POST'})


# Login user

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(phone_number=request.POST.get('phone_number')).first():
            user_phone = request.POST.get('phone_number')
            user = authenticate(request, phone_number=user_phone, password=request.POST.get('password'))
            if user is None:
                return JsonResponse(
                    {'status': 'error', 'message': 'Could not login. Please check your password', 'status_code': 400},
                    status=400)
            else:
                current_user = CustomUser.objects.get(phone_number=request.POST.get('phone_number'))
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                return JsonResponse({'status': 'success', 'message': 'Success, welcome back', 'token': str(token),
                                     'username': str(current_user.username), 'user_id': str(current_user.id),
                                     'status_code': 200}, status=200)
        return JsonResponse(
            {'status': 'error', 'message': "This phone_number doesn't exists. Create a new account or check your sms",
             'status_code': 404},
            status=404)
    else:
        return JsonResponse({'status': 'not POST'})


# Change current password
@csrf_exempt
def change_current_password(request):
    if request.method == 'POST':
        user = authenticate(request, phone_number=request.POST.get('phone_number'),
                            password=request.POST.get('current_password'))
        if user is None:
            return JsonResponse(
                {'status': 'error', 'message': 'incorrect password reset password if you dont remember',
                 'status_code': 400},
                status=400)
        else:
            user.set_password(request.POST.get('new_password'))
            user.save()
            token = Token.objects.filter(user=user)
            new_key = token[0].generate_key()
            token.update(key=new_key)
            new_token = Token.objects.get(user=user)
            return JsonResponse(
                {'status': 'success', 'message': 'Password changed successfully', 'token': str(new_token),
                 'username': str(user.username), 'user_id': str(user.id), 'status_code': 200},
                status=200)


# Forget password
@csrf_exempt
def forget_password_send_0TP(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).first():
            verification_code = generateOTP()
            user = CustomUser.objects.get(phone_number=phone_number)
            if OTP.objects.filter(user=user).exists():
                current_otp = OTP.objects.filter(user=user)
                for available_otp in current_otp:
                    available_otp.delete()

            otp_model = OTP()

            otp_model.user = user
            otp_model.otp_value = verification_code
            otp_model.save()

            message = f'Hello, \n recently you requested to reset your password. Here is your verification code to reset your SpareTz account. \n {verification_code}.\n \n'
            try:
                send_sms_message(phone_number, message)
                return JsonResponse({'status': 'success', 'message': 'Password reset sent successfully check your sms',
                                     'status_code': 200}, status=200)

            except BadHeaderError:
                return HttpResponse('Invalid Header.')
        else:
            return JsonResponse(
                {'status': 'error', 'message': "This phone number doesn't exists", 'status_code': 404, },
                status=404)


# Verify user email
@csrf_exempt
def verify_user_send_OTP(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).first():
            verification_code = generateOTP()
            user = CustomUser.objects.get(phone_number=phone_number)
            if OTP.objects.filter(user=user).exists():
                current_otp = OTP.objects.filter(user=user)
                for available_otp in current_otp:
                    available_otp.delete()

            otp_model = OTP()

            otp_model.user = user
            otp_model.otp_value = verification_code
            otp_model.save()
            user_phone_number = user.phone_number
            print(user_phone_number)
            message = f'Hello, \n welcome to  SpareTz. Here is your verification code \n {verification_code}\n If you didnt request this, forget about it and report.'
            try:
                send_sms_message(user_phone_number, message)
                return JsonResponse(
                    {'status': 'success', 'message': 'verification code sent successfully check your sms',
                     'status_code': 200, 'otp': verification_code},
                    status=200)

            except BadHeaderError:
                return HttpResponse('Invalid Header.')
        else:
            return JsonResponse({'status': 'error', 'message': "This phone number doesn't exists", 'status_code': 404, },
                                status=404)


# Verify forget password otp
@csrf_exempt
def verify_forget_password_otp(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(phone_number=request.POST.get('phone_number'))
        if OTP.objects.filter(user=user, otp_value=request.POST.get('otp_value')).exists():
            current_otp = OTP.objects.filter(user=user)
            for available_otp in current_otp:
                available_otp.delete()
            return JsonResponse(
                {'status': 'success', 'message': 'verification code verified successfully',
                 'status_code': 200},
                status=200)

        else:
            return JsonResponse({'status': 'error', 'message': "Invalid verification code ", 'status_code': 404, },
                                status=404)


# Verify  signup otp
@csrf_exempt
def verify_signup_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)
        if OTP.objects.filter(user=user, otp_value=request.POST.get('otp_value')).exists():
            current_otp = OTP.objects.filter(user=user)
            for available_otp in current_otp:
                available_otp.delete()
            current_user = CustomUser.objects.get(phone_number=phone_number)
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse(
                {'status': 'success', 'message': 'verification code verified successfully', 'token': str(token),
                 'username': str(current_user.username), 'user_id': str(current_user.id),
                 'status_code': 200}, status=200)


        else:
            return JsonResponse({'status': 'error', 'message': "Invalid verification code ", 'status_code': 404, },
                                status=404)


# Change forget password
@csrf_exempt
def change_forget_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)
        user.set_password(request.POST.get('new_password'))
        user.save()
        token = Token.objects.filter(user=user)
        new_key = token[0].generate_key()
        token.update(key=new_key)
        new_token = Token.objects.get(user=user)
        return JsonResponse(
            {'status': 'success', 'message': 'Password changed successfully', 'token': str(new_token),
             'username': str(user.username), 'user_id': str(user.id), 'status_code': 200},
            status=200)


@csrf_exempt
def delete_user_data(request):
    user_id = request.POST.get('user_id')
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        # Any additional cleanup or related data deletion can be performed here
        return JsonResponse(
            {'status': 'success', 'message': 'Account Deleted successfully', 'status_code': 200},
            status=200)
    except User.DoesNotExist:
        # Handle case when the user doesn't exist
        return JsonResponse({'status': 'error', 'message': "User doesn't exist ", 'status_code': 404, },
                                status=404)