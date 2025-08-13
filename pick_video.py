from googleapiclient.discovery import build  # Import function to build Google API service clients
import csv  # Import CSV module for writing data to CSV files

# 1. YouTube API setup
API_KEY = 'AIzaSyA7lmu_1fK5ywKtrIIo0bPwKOz8G1-2Xag'  # Your YouTube Data API key for authentication

# Build the YouTube API client (version 3) using the API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to search for YouTube videos based on a query (search term)
def search_videos_by_title(query, max_results=1):
    # Create a search request to YouTube API with specific parameters:
    request = youtube.search().list(
        part="snippet",            # Request video metadata like title, description, channel, publish date
        q=query,                   # The search query string provided as function argument
        type="video",              # Limit search results to videos only (exclude channels/playlists)
        maxResults=max_results,    # Maximum number of results to return (default is 1)
        order="viewCount"          # Sort the results by view count (most popular first)
    )
    response = request.execute()   # Send the request and get the response from YouTube API

    videos = []  # Initialize an empty list to store video info
    # Loop through each video item returned by the API
    for item in response['items']:
        video_id = item['id']['videoId']             # Extract the video ID
        video_url = f"https://www.youtube.com/watch?v={video_id}"  # Build full video URL
        title = item['snippet']['title']              # Extract the video title
        published_at = item['snippet']['publishedAt'] # Extract the publish date/time
        channel_title = item['snippet']['channelTitle'] # Extract the channel's name
      
        # Add this video's info as a dictionary to the videos list
        videos.append({
            'video_id': video_id,
            'video_url': video_url,
            'title': title,
            'published_at': published_at,
            'channel_title': channel_title
        })
    return videos  # Return the list of video dictionaries

# Function to save a list of dictionaries into a CSV file
def save_to_csv(data, filename='youtube_videos.csv'):
    keys = data[0].keys()  # Extract the dictionary keys to use as CSV header columns
    # Open the CSV file for writing (UTF-8 encoding to support all characters)
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)  # Create writer object
        dict_writer.writeheader()  # Write the CSV header row
        dict_writer.writerows(data) # Write all video dictionaries as rows

# 4. Execute the search and save the results
query = "YAMAHA TRACER 9"             # Define your search term here
videos = search_videos_by_title(query, max_results=5) # You can increase max_results

save_to_csv(videos)                    # Save the retrieved videos info into a CSV file

# Print how many videos were saved to the CSV
print(f"Saved {len(videos)} videos to youtube_videos.csv")
