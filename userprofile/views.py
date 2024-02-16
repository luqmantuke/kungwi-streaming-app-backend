from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myauthentication.serializers import UserSerializer
from myauthentication.models import CustomUser
from purchase.models import Purchase
from .models import UserProfile


@csrf_exempt
def fetch_user_profile(request):
    try:

        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        user_serializer = UserSerializer(user).data
        return JsonResponse(
            {'status': 'success', 'message': 'User Fetched successfully', 'status_code': 200, 'data': user_serializer})

    except:
        return JsonResponse(
            {'status': 'error', 'message': 'User hasn\'t logged in', 'status_code': 400, })


@csrf_exempt
def user_purchased_story(request):
    try:
        user_id = request.POST.get('user_id')
        story_type = request.POST.get('story_type')
        story_id = request.POST.get('story_id')
        purchases = Purchase.objects.filter(story_type=story_type, story_id=story_id, user__id=user_id,
                                            is_success=True).exists()
        print(purchases)
        if purchases:
            return JsonResponse(
                {'status': 'success', 'message': 'User purchased this story', 'status_code': 200, })
        else:
            return JsonResponse(
                {'status': 'error', 'message': 'User hasn\'t purchased', 'status_code': 400, })
    except:
        return JsonResponse(
            {'status': 'error', 'message': 'User hasn\'t logged in', 'status_code': 400, })
