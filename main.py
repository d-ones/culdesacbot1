import time
import urllib.parse
import requests
import os
import tweepy
import creds
import random

# Variables

auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
auth.set_access_token(creds.access_token, creds.access_secret)
posturl = '&zoom=20&maptype=satellite&size=640x640&key='
baseurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
api = tweepy.API(auth)

# Establishing lists

# List of all coordinates

with open('shufflecoords.csv', newline='')as f:
    coordrows = f.readlines()
    coordlines = [coordrow.rstrip() for coordrow in coordrows]
    f.close()

# List of used coordinates

with open('used.txt', 'r') as fd:
    usedrows = fd.readlines()
    usedlines = [usedrow.rstrip() for usedrow in usedrows]
    fd.close()

# Removing used from all coords

for element in usedlines:
    if element in coordlines:
        coordlines.remove(element)

# Start of actual tweeting function

for coord in coordlines:

    try:

        usedlines.append(str(coord))
        with open('used.txt', 'w') as out:
            for line in usedlines:
                out.write(f'{line}\n')

        #Generate Content

        text = coord.split(',')
        lat = (text[0])
        lon = str(text[1])
        nom = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&zoom=11&format=json'
        locate = requests.get(nom)
        json = locate.json()
        location = json['display_name']
        url = (baseurl + urllib.parse.quote_plus((str(coord))) + posturl + creds.maps_api)
        response = requests.get(url)
        imagesave = f'tempscreenshot{len(coordlines)}.png'
        with open(f'{imagesave}', 'wb') as image:
            image.write(response.content)

        # Twitter API stuff

        image_path = f'tempscreenshot{len(coordlines)}.png'
        tweet_text = f'{location}\n{lat}, {lon}'
        api.update_status_with_media(tweet_text, image_path)

        # Delete and sleep

        os.remove(f'tempscreenshot{len(coordlines)}.png')

        # Don't delete this :-) !

        time.sleep(3600)

    except ValueError:
        break
