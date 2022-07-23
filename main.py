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
usedfile = '/var/bot/used.txt'

# Check if used works

if not os.path.exists(usedfile):
    print('Creating Used File')
    with open(usedfile, 'w'):
        pass

# Establishing lists

# List of all coordinates

with open('shufflecoords.csv', newline='')as f:
    coordrows = f.readlines()
    coordlines = [coordrow.rstrip() for coordrow in coordrows]

# List of used coordinates

with open(usedfile, 'r') as fd:
    usedrows = fd.readlines()
    usedlines = [usedrow.rstrip() for usedrow in usedrows]

# Removing used from all coords

print(f'Removing used ({len(usedlines)} of {len(coordlines)})')

for element in usedlines:
    if element in coordlines:
        coordlines.remove(element)

print(f'Untweeted: {len(coordlines)}')

# Start of actual tweeting function

print('Beginning')

for coord in coordlines:

    print(f'Tweeting {str(coord)}')

    # Write used

    with open(usedfile, 'a') as out:
        out.write(f'{str(coord)}\n')
    print('Used file updated')

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
    print('Image saved')

    # Twitter API stuff

    image_path = f'tempscreenshot{len(coordlines)}.png'
    tweet_text = f'{location}\n{lat}, {lon}'
    api.update_status_with_media(tweet_text, image_path)
    print('Tweet posted')

    # Delete and sleep

    os.remove(f'tempscreenshot{len(coordlines)}.png')
    print('Image deleted')

    # Don't delete this :-) !

    print('Sleeping')

    time.sleep(3600)
