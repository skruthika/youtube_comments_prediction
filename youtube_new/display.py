from flask import Flask, request, render_template

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

API_KEY = "AIzaSyBUO3Ng21xrXepEwabtdbb18-8A2Aj5_78"  # Replace with your YouTube API key


def search_videos(query):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_ids = []

    try:
        request = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet'
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_ids.append((video_id, video_title))

    except HttpError as e:
        print(f'An error occurred: {e}')

    return video_ids

def get_video_comments(api_key, video_id, max_comments=10):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=max_comments
        )
        response = request.execute()

        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        return comments

    except HttpError as e:
        print(f'An error occurred while fetching comments: {e}')
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        video_ids_list = search_videos(search_query)

        if video_ids_list:
            first_video_id, first_video_title = video_ids_list[0]
            comments = get_video_comments(API_KEY, first_video_id)

            return render_template('index.html', video_title=first_video_title, comments=comments)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
