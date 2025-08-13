import pick_video
from comment_collector import collect_and_save_comments
import analyze_youtube_comments
from video_summary import get_video_summar

import pandas as pd
import sys
import os
import streamlit as st

def run_video_search(query):
    videos = pick_video.search_videos_by_title(query)
    pick_video.save_to_csv(videos)
    print("Videos picked and saved to youtube_videos.csv")
    return len(videos)

def analyze_comments():
    analyze_youtube_comments.main()
    print("Comments analyzed and summaries saved")

def run_cli():
    query = "YAMAHA TRACER 9"
    print(f"Running pipeline for query: {query}")
    n_videos = run_video_search(query)

    video_data = pd.read_csv('youtube_videos.csv')
    video_ids = video_data['video_id'].tolist()

    n_comments = collect_and_save_comments(video_ids)
    print(f"Collected {n_comments} comments.")

    analyze_comments()

def run_ui():
    st.title("YouTube Comments Analysis Tool")

    query = st.text_input("Enter search query:", "YAMAHA TRACER 9")

    if st.button("Run pipeline"):
        if not query.strip():
            st.error("Please enter a search query")
            return

        st.info(f"Searching videos for: {query}")
        n_videos = run_video_search(query)
        st.success(f"Found {n_videos} videos.")

        video_data = pd.read_csv('youtube_videos.csv')
        video_ids = video_data['video_id'].tolist()

        st.info("Collecting comments...")
        n_comments = collect_and_save_comments(video_ids)
        st.success(f"Collected {n_comments} comments.")

        st.info("Analyzing comments...")
        analyze_comments()
        st.success("Analysis complete!")

        # After analysis, show all theme summary files in the UI
        st.header("Analysis Summaries")

        base_path = os.path.abspath('.')
        summary_files = [f for f in os.listdir(base_path) if f.endswith("_theme_summary.txt")]

        if not summary_files:
            st.warning("No summary files found.")
        else:
            for file in summary_files:
                st.subheader(f"Summary: {file}")
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        st.text_area(label=f"Contents of {file}", value=content, height=300)
                except Exception as e:
                    st.error(f"Could not read {file}: {e}")

if __name__ == "__main__":
    # Run with: python main.py  (for CLI)
    # Or run UI: streamlit run main.py -- --ui
    if len(sys.argv) > 1 and sys.argv[1] == "--ui":
        run_ui()
    else:
        run_cli()
