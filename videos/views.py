from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *


@csrf_exempt
def fetch_trending_videos(request):
    trending_videos = Videos.objects.filter(is_trending=True)
    videos_serializer = VideoSerializer(trending_videos, many=True).data
    return JsonResponse(
        {'status': 'success', 'message': 'Trending Videos pulled successfully', 'data': list(videos_serializer),
         'status_code': 200}, status=200)


@csrf_exempt
def fetch_all_videos(request):
    all_videos = Videos.objects.all()
    videos_serializer = VideoSerializer(all_videos, many=True).data
    return JsonResponse(
        {'status': 'success', 'message': 'Videos pulled successfully', 'data': list(videos_serializer),
         'status_code': 200}, status=200)

@csrf_exempt
def fetch_trending_series(request):
    trending_series = Series.objects.filter(is_trending=True)
    series_serializer = SeriesSerializer(trending_series, many=True).data
    return JsonResponse(
        {'status': 'success', 'message': 'Trending Series pulled successfully', 'data': list(series_serializer),
         'status_code': 200}, status=200)


@csrf_exempt
def fetch_series_with_episodes(request):
    series_id = request.POST.get('series_id')
    try:
        series = Series.objects.get(id=series_id)
        series_serializer = SeriesSerializer(series).data
        return JsonResponse(
            {'status': 'success', 'message': 'Series with Episodes pulled successfully', 'data': series_serializer,
             'status_code': 200}, status=200)
    except Series.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Series not found', 'status_code': 404}, status=404)

@csrf_exempt
def fetch_all_series(request):
    all_series = Series.objects.all()
    series_serializer = SeriesSerializer(all_series, many=True).data
    return JsonResponse(
        {'status': 'success', 'message': 'Series pulled successfully', 'data': list(series_serializer),
         'status_code': 200}, status=200)

