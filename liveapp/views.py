import os
import subprocess
import httpx
from datetime import datetime, timezone
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse, Http404
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

UTC = timezone.utc

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_BUCKET = os.getenv('SUPABASE_BUCKET')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Homepage view
def homepage(request):
    return render(request, 'responsive.html')

# Fetch video and stream it
def stream_video(request, filename):
    try:
        video_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(filename)
    except Exception as e:
        return HttpResponse("Failed to fetch video list", status=500)

    async def video_stream():
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url, follow_redirects=True)
            if response.status_code != 200:
                raise Http404("Failed to fetch video")

            async for chunk in response.aiter_bytes(chunk_size=8192):
                yield chunk

    return StreamingHttpResponse(video_stream(), content_type="video/mp4")

# Get a video URL
def get_video(request, video_name):
    video_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(video_name)

    if not video_url:
        return JsonResponse({'error': 'Video not found'}, status=404)

    async def video_stream():
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url, headers={'Range': 'bytes=0-'}, timeout=None, follow_redirects=True)
            if response.status_code not in [200, 206]:
                raise Http404("Failed to fetch video")
            async for chunk in response.aiter_bytes(chunk_size=8192):
                yield chunk    

    return StreamingHttpResponse(video_stream(), content_type="video/mp4")

# Convert MP4 to M3U8 using FFmpeg
def go_live(request):
    try:
        subprocess.run(['ffmpeg', '-i', 'input.mp4', 'output.m3u8'], check=True)
        return JsonResponse({'message': 'Conversion successful'})
    except subprocess.CalledProcessError:
        return JsonResponse({'error': 'Conversion failed'}, status=500)
