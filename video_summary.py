import yt_dlp
import whisper
import os
import subprocess
import re


def download_audio(youtube_url, output_path="audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.splitext(output_path)[0],  # remove extension
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def get_video_title(youtube_url):
    ydl_opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict.get('title', 'Unknown Title')


def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # change to "tiny" for faster, less accurate
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_with_llama(text, title, model_name="llama3.2:1b"):
    prompt = f"""Video title: {title}

Here is the transcript of the video. Summarize it into clear bullet points that highlight the key ideas and main takeaways.

Transcript:
{text}
"""
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode("utf-8").strip()


def chunk_text(text, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_video(url):
    try:
        title = get_video_title(url)
        
        # Create safe folder
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
        folder_path = os.path.join("summaries", safe_title)
        os.makedirs(folder_path, exist_ok=True)
        print(f"\nVideo title: {title}")

        audio_file = "audio.mp3"

        print("Downloading audio...")
        download_audio(url, audio_file)
        print("Download complete.")

        print("Transcribing audio with Whisper...")
        transcript = transcribe_audio(audio_file)
        print("\n--- Transcription ---\n")
        print(transcript)

        print("\nSummarizing transcript with LLaMA...")
        chunks = chunk_text(transcript)
        chunk_summaries = [summarize_with_llama(c, title) for c in chunks]
        final_summary = summarize_with_llama("\n".join(chunk_summaries), title)

        print("\n--- Summary ---\n")
        print(final_summary)

        #summary_file = os.path.join(folder_path, "summary.txt")
        #with open(summary_file, "w", encoding="utf-8") as f:
        #  f.write(final_summary)

        # Optional: cleanup
        if os.path.exists(audio_file):
            os.remove(audio_file)

        return final_summary
    except Exception as e:
        return f"Error during summarization: {e}"

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Replace with a default video URL
    summary = summarize_video(url)
    print(summary)
