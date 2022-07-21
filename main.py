import time
import urllib.parse
import requests
import os
import tweepy
import creds
import pandas as pd

# Variables

auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_secret)
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
api = tweepy.API(auth)

# https://pythonspeed.com/articles/pandas-read-csv-fast/
# Engine PyArrow give us better performance than default engine in reading
df = pd.read_csv('culdesaccoords2021.csv', engine="pyarrow")

while True:
    try:
        # Generate Content
        random_coord = df.sample(1)  # pick single random sample
        coord_array = random_coord.\
            to_string(header=False, index=False, index_names=False).split(" ")
        coord_str = " , ".join(coord_array)
        lat: str = coord_array[0]
        lon: str = coord_array[1][:-2]
        nom = \
            f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&zoom=11&format=json'
        locate = requests.get(nom)
        json = locate.json()
        location = json['display_name']
        url: str = baseurl + \
            urllib.parse.quote_plus((coord_str)) + posturl + creds.maps_api
        response = requests.get(url)
        len_line = len(lat) + len(lon) + 1
        imagesave = f'tempscreenshot{len_line}.png'
        with open(f'{imagesave}', 'wb') as image:
            image.write(response.content)

        # Put in Twitter API stuff

        image_path: str = f'tempscreenshot{len_line}.png'
        tweet_text: str = f'{location}\n{coord_str}'
        api.update_status_with_media(tweet_text, image_path)

        # Delete and sleep

        os.remove(f'tempscreenshot{len_line}.png')
        df.drop(random_coord.index[0], inplace=True)

        # Overwrite this new data to existing CSV file
        df.to_csv('culdesaccoords2021.csv', sep=',', index=False, header=False)

        # Don't delete this :-) !
        time.sleep(1800)
    except ValueError:  # no entry left for randomize
        break
