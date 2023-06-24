import os
import json
import requests


API_KEY = os.environ.get('YOUTUBEAPI')
BASE_URL = "https://www.googleapis.com/youtube/v3"
country_code = input("Enter country code (ex. US, CA): ")
part = "snippet,contentDetails,statistics"

url = f"{BASE_URL}/videos?part={part}&chart=mostPopular&regionCode={country_code}&maxResults=3&key={API_KEY}"

response = requests.get(url)

data = response.json()

videos = data["items"]

print(f"""

Popular Videos in {country_code}:""")

for video in videos:
    title = video["snippet"]["title"]
    description = video["snippet"]["description"][:200]
    channel = video["snippet"]["channelTitle"]
     
    if "tags" in video["snippet"]:
        tags = video["snippet"]["tags"]
    else:
        tags = "None"

    views = video["statistics"]["viewCount"]
    likes = video["statistics"]["likeCount"]
    comments = video["statistics"]["commentCount"]
    print(
      f"""
      Title: {title}
      Description: {description}...
      Channel: {channel}
      Tags: {tags}
      Views: {views}
      Likes Count: {likes}
      Comments Count: {comments}
      """)
