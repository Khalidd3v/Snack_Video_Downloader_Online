from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import StreamingHttpResponse , HttpResponse
from urllib.parse import quote, unquote  # Add unquote import

def get_video_info(video_url):
    response = requests.get(video_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        video_tag = soup.find('video')
        if video_tag:
            video_src = video_tag['src']
            return video_src
    return None

def homepage(request):
    if request.method == 'POST':
        video_url = request.POST.get('video_url')
        if video_url:
            video_src = get_video_info(video_url)
            if video_src:
                video_src_decoded = unquote(video_src)  # Decode the URL
                context = {'video_src': video_src_decoded}
                return render(request, 'app/video_download.html', context)

    return render(request, 'app/homepage.html')

def download_video(request, video_src):
    if video_src:
        response = requests.get(video_src, stream=True)

        if response.status_code == 200:
            file_size = int(response.headers['Content-Length'])
            response = StreamingHttpResponse(
                response.iter_content(chunk_size=8192),
                content_type='video/mp4'
            )
            response['Content-Disposition'] = 'attachment; filename="video.mp4"'
            response['Content-Length'] = file_size
            return response
        else:
            return HttpResponse("Failed to download video.", status=404)
    else:
        return HttpResponse("No valid video source URL to download.", status=404)