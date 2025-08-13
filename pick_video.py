from googleapiclient.discovery import build
import csv

API_KEY = 'AIzaSyA7lmu_1fK5ywKtrIIo0bPwKOz8G1-2Xag'  # Keep it secure, don't hardcode in production
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos_by_title(query, max_results=5):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        order="viewCount"
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']
        channel_title = item['snippet']['channelTitle']

        videos.append({
            'video_id': video_id,
            'video_url': video_url,
            'title': title,
            'published_at': published_at,
            'channel_title': channel_title
        })
    return videos

def save_to_csv(data, filename='youtube_videos.csv'):
    if not data:
        print("No videos to save.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
