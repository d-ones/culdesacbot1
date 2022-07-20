import random
import time
import urllib.parse
import requests
import os
import tweepy
import creds

# Variables

auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_secret)
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
api = tweepy.API(auth)

# Read coords into list

with open('culdesaccoords2021.csv', newline='')as f:
    lines = f.readlines()

for line in lines:

            #Generate Content

            coord = random.choice(lines)
            text = coord.split(',')
            lat = (text[0])
            lon = str(text[1][:-2])
            nom = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&zoom=11&format=json'
            locate = requests.get(nom)
            json = locate.json()
            location = json['display_name']
            url = (baseurl + urllib.parse.quote_plus((str(coord))) + posturl + creds.maps_api)
            response = requests.get(url)
            imagesave = f'tempscreenshot{len(lines)}.png'
            with open(f'{imagesave}', 'wb') as image:
                image.write(response.content)

            # Put in Twitter API stuff

            image_path = f'tempscreenshot{len(lines)}.png'
            tweet_text = f'{location}\n{str(coord)}'
            api.update_status_with_media(tweet_text, image_path)

            # Delete and sleep

            os.remove(f'tempscreenshot{len(lines)}.png')
            lines.remove(coord)

            # Don't delete this :-) !

            time.sleep(1800)
