from googleapiclient.discovery import build
import pandas as pd
import os

# 1. API setup
API_KEY = 'AIzaSyA7lmu_1fK5ywKtrIIo0bPwKOz8G1-2Xag'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 2. Function to get comments
def get_comments(video_id, max_comments=5):
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=5,
            pageToken=next_page_token,
            textFormat='plainText'
        )
        response = request.execute()

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': comment['authorDisplayName'],
                'text': comment['textDisplay'],
                'published_at': comment['publishedAt'],
                'like_count': comment['likeCount']
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return comments

# 3. Function to loop through each video ID and save comments
def collect_and_save_comments(video_ids, max_comments_per_video=5):
    total_comments = 0
    for video_id in video_ids:
        print(f"Processing video: {video_id}")
        try:
            comments = get_comments(video_id, max_comments=max_comments_per_video)
            df = pd.DataFrame(comments)
            filename = f'comments_{video_id}.csv'
            df.to_csv(filename, index=False)
            print(f"Saved {len(comments)} comments to {filename}")
            total_comments += len(comments)
        except Exception as e:
            print(f"Failed to process {video_id}: {e}")
    return total_comments

if __name__ == "__main__":
    # Load video IDs from CSV and run the collection process
    if os.path.exists('youtube_videos.csv'):
        video_data = pd.read_csv('youtube_videos.csv')
        video_ids = video_data['video_id'].tolist()
        collect_and_save_comments(video_ids)
    else:
        print("youtube_videos.csv not found. Please run pick_video.py first.")
