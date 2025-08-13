import pick_video
from comment_collector import collect_and_save_comments
import analyze_youtube_comments
import video_summary

import pandas as pd
import os


def run_video_search(query):
    videos = pick_video.search_videos_by_title(query)
    pick_video.save_to_csv(videos)

    # Add video summaries
    video_data = pd.read_csv('youtube_videos.csv')
    video_data['summary'] = video_data['video_url'].apply(video_summary.summarize_video)
    video_data.to_csv('youtube_videos.csv', index=False)

    print("Videos picked and saved to youtube_videos.csv with summaries")
    return len(videos)


def analyze_comments():
    analyze_youtube_comments.main()
    print("Comments analyzed and summaries saved")


def run_cli():
    query = input("Enter search query: ").strip()
    if not query:
        print("You must enter a search query.")
        return

    print(f"\nRunning pipeline for query: {query}")
    n_videos = run_video_search(query)
    print(f"Found {n_videos} videos.")

    video_data = pd.read_csv('youtube_videos.csv')
    video_ids = video_data['video_id'].tolist()

    # Collect comments
    print("\nCollecting comments...")
    n_comments = collect_and_save_comments(video_ids)
    print(f"Collected {n_comments} comments.")

    # Analyze comments
    print("\nAnalyzing comments...")
    analyze_comments()

    # Show summary files if any
    print("\n--- Analysis Summaries ---")
    base_path = os.path.abspath('.')
    summary_files = [f for f in os.listdir(base_path) if f.endswith("_theme_summary.txt")]

    if not summary_files:
        print("No summary files found.")
    else:
        for file in summary_files:
            print(f"\nSummary: {file}")
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Could not read {file}: {e}")


if __name__ == "__main__":
    run_cli()
