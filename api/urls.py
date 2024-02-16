from firebasekijiweni.views import create_update_firebase
from myauthentication.views import *
from django.urls import path, include

from purchase.views import *
from userprofile.views import *
from firebasekijiweni.views import *
from videos.views import *
urlpatterns = [
    # videos
    path('fetch_trending_videos/', fetch_trending_videos),
    path('fetch_trending_series/', fetch_trending_series),
    path('fetch_series_with_episodes/', fetch_series_with_episodes),
    path('fetch_all_series/', fetch_all_series),
    path('fetch_all_videos/', fetch_all_videos),

    # firebase
    path("send_notification_single_user/",send_notification_single_user),
    path('create_update_firebase/', create_update_firebase),

    path('create_purchase_order/', create_purchase_order),
    path('webhook_payment_endpoint/', webhook_payment_endpoint),
    path('create_buy_credit_order/', create_buy_credit_order),
    path('create_buy_credit_order/', create_buy_credit_order),
    path('webhook_buy_credit_endpoint/', webhook_buy_credit_endpoint),
    path('fetch_user_profile/', fetch_user_profile),
    path('user_purchased_story/', user_purchased_story),
    path('is_monetization_on/', is_monetization_on),
    path('fetch_vifurushi/', fetch_vifurushi),
    path('buy_story/', buy_story),
    path('auth/signup/', signup),
    path('auth/login/', login),
    path('auth/change_current_password/', change_current_password),
    path('auth/verify_forget_password_otp/', verify_forget_password_otp),
    path('auth/verify_signup_otp/', verify_signup_otp),
    path('auth/change_forget_password/', change_forget_password),
    path('rest/', include('rest_framework.urls')),

]