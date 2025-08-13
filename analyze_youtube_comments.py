import os
import pandas as pd
from collections import Counter
import subprocess

def generate_with_ollama(prompt, model_name="llama3.2:1b"):
    cmd = ["ollama", "run", model_name]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # Use UTF-8 encoding explicitly
    )
    stdout, stderr = process.communicate(input=prompt)

    if stderr and "Error" in stderr:
        print("Ollama error:", stderr)
        return None

    return stdout.strip()


def classify_comment_theme(comment):
    prompt = f"""
Classify the following comment into one clear theme.

Choose from: 
- Praise
- Complaint
- Question
- Thanks
- Suggestion
- Joke
- Off-topic
- Neutral / unclear

Examples:
Comment: "I love this video, great work!"
Category: Praise

Comment: "Why does this feature not work?"
Category: Question

Comment: "Thanks for sharing this information."
Category: Thanks

Comment: "This is so funny lol"
Category: Joke

Comment: "The product arrived late."
Category: Complaint

Now classify this comment:

Comment: "{comment}"

Respond with only the category name.
"""
    response = generate_with_ollama(prompt)
    if response:
        return response.lower()
    else:
        return "error"

def summarize_theme(df, theme, summary_file):
    comments = df[df['theme'] == theme]['text'].tolist()
    if len(comments) == 0:
        return

    prompt = f"""
The following YouTube comments fall under the theme "{theme.title()}".

Please summarize the main ideas, topics, or patterns observed in these comments using 3–5 bullet points.

Comments:
{chr(10).join(comments)}

Respond only with bullet points.
"""
    summary = generate_with_ollama(prompt)
    if summary:
        with open(summary_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n--- Insights for theme: {theme.title()} ---\n")
            f.write(summary)
    else:
        print(f"Error summarizing theme '{theme}'.")

def main():
    comment_files = [f for f in os.listdir('.') if f.startswith("comments_") and f.endswith(".csv")]

    for file in comment_files:
        print(f"Processing: {file}")
        df = pd.read_csv(file)
        df['text'] = df['text'].fillna('')

        theme_counts = Counter()
        theme_list = []

        for idx, row in df.iterrows():
            comment = row['text']
            theme = classify_comment_theme(comment)
            theme_list.append(theme)
            theme_counts[theme] += 1
            print(f"[{idx+1}/{len(df)}] Theme: {theme}")
            # Optional: time.sleep(0.5)

        df['theme'] = theme_list
        df.to_csv(file, index=False)
        print(f"Updated: {file} with theme classifications")

        summary_file = file.replace('.csv', '_theme_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Theme Summary for {file} ===\n\n")
            total_comments = sum(theme_counts.values())
            for theme, count in theme_counts.most_common():
                pct = (count / total_comments) * 100
                f.write(f"- {theme.title()}: {count} ({pct:.1f}%)\n")

        print(f"Saved summary: {summary_file}")

        for theme in theme_counts:
            summarize_theme(df, theme, summary_file)

        print(f"Added summaries for each theme.\n")

if __name__ == "__main__":
    main()
