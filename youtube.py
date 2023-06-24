import os
import json
import requests
import sqlalchemy as db
import pandas as pd

API_KEY = os.environ.get('YOUTUBEAPI')
BASE_URL = "https://www.googleapis.com/youtube/v3"
country_code = input("Enter country code (ex. US, CA): ")
part = "snippet,contentDetails,statistics"

url = f"{BASE_URL}/videos?part={part}&chart=mostPopular&regionCode={country_code}&maxResults=10&key={API_KEY}"

response = requests.get(url)

data = response.json()

videos = data["items"]

print(f"""

Popular Videos in {country_code}:""")

youtubevideos = pd.DataFrame({
    "Title": [],
    "Description": [],
    "Channel": [],
    "Tags": [],
    "Views": [],
    "Likes Count": [],
    "Comments Count": []})


for video in videos:
    title = video["snippet"]["title"]

    description = video["snippet"]["description"][:200] + ".."
    channel = video["snippet"]["channelTitle"]
     
    if "tags" in video["snippet"]:
        tags = video["snippet"]["tags"]
    else:
        tags = "None"

    views = video["statistics"]["viewCount"]
    likes = video["statistics"]["likeCount"]
    comments = video["statistics"]["commentCount"]
    
    row = {"Title": title, "Description": description,
      "Channel": channel, "Tags": str(tags),
      "Views": views, "Likes Count": likes,
      "Comments Count": comments}
   
    youtubevideos.loc[len(youtubevideos)] = row
    print(
      f"""
      Title: {title}
      Description: {description}
      Channel: {channel}
      Tags: {tags}
      Views: {views}
      Likes Count: {likes}
      Comments Count: {comments}
      """)

engine = db.create_engine('sqlite:///youtubevideos.db')
youtubevideos.to_sql("popular", con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM popular;")).fetchall()
   print(pd.DataFrame(query_result))