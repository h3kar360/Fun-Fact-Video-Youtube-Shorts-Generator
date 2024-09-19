from moviepy.editor import *
from moviepy.video.fx.all import speedx
from moviepy.config import change_settings
import requests
from gtts import gTTS
import env

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

def findLenFact():
    arrChoice = []
    api_url = 'https://api.api-ninjas.com/v1/facts'
    response = requests.get(api_url, headers={ 'X-Api-Key': env.API_KEY })
    if response.status_code == requests.codes.ok:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)

    fact = data[0]["fact"] 
    splitStr = fact.split(' ')

    if len(splitStr) >= 10:
        newSplit = []
        for i in range(0, len(splitStr)):
            newSplit.append(splitStr[i])
            if (i+1)%4 == 0:
                newSplit.append('\n')
    
        combinedSplit = ' '.join(newSplit)  

        arrChoice.append(combinedSplit)    
        arrChoice.append(fact)  
        return arrChoice
    else:
        return findLenFact()
    
fact = findLenFact()
speech = 'fun fact, ' + fact[1]

convertTS = gTTS(text=speech, lang='en-uk', slow=False)

convertTS.save('audio/randFacts.mp3')

def get_background():
    query = 'nature'
    url = f'https://api.unsplash.com/photos/random/?client_id={env.CLIENT_ID}&query={query}&orientation=portrait'

    res = requests.get(url)
    data = res.json()

    imgURL = data['urls']['raw']

    custom_width = 1080
    custom_height = 1920
    custom_image_url = f'{imgURL}&w={custom_width}&h={custom_height}'

    img_res = requests.get(custom_image_url)

    with open('background/background.png', 'wb') as f:
        f.write(img_res.content)

get_background()

res = requests.get(f'https://api.deezer.com/search/track?q=pop&order=RANKING&limit=50')
data = res.json()
rand = random.randint(0, 49)
track_url = data['data'][rand]['preview']

audRes = requests.get(track_url)
with open('audio/bg_music.mp3', 'wb') as file:
    file.write(audRes.content)

audio = AudioFileClip('audio/randFacts.mp3').volumex(1.2)
spedAud = speedx(audio, factor=1.2)

duration = spedAud.duration

bgMusic = AudioFileClip('audio/bg_music.mp3').volumex(0.1).set_duration(duration);

combAud = CompositeAudioClip([spedAud, bgMusic])

background = ImageClip('background/background.png').set_duration(duration)

text = TextClip(fact[0], fontsize=70, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2).set_position('center').set_duration(duration).crossfadein(1)    

background = background.set_audio(combAud)

video = CompositeVideoClip([background, text])

video.write_videofile('facts.mp4', fps=24)

# # Explicitly tell the underlying HTTP transport library not to retry, since
# # we are handling retry logic ourselves.
# httplib2.RETRIES = 1

# # Maximum number of times to retry before giving up.
# MAX_RETRIES = 10

# # Always retry when these exceptions are raised.
# RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# # Always retry when an apiclient.errors.HttpError with one of these status
# # codes is raised.
# RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# # the OAuth 2.0 information for this application, including its client_id and
# # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# # the Google API Console at
# # https://console.cloud.google.com/.
# # Please ensure that you have enabled the YouTube Data API for your project.
# # For more information about using OAuth2 to access the YouTube Data API, see:
# #   https://developers.google.com/youtube/v3/guides/authentication
# # For more information about the client_secrets.json file format, see:
# #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# CLIENT_SECRETS_FILE = "client_secrets.json"

# # This OAuth 2.0 access scope allows an application to upload files to the
# # authenticated user's YouTube channel, but doesn't allow other types of access.
# YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

# # This variable defines a message to display if the CLIENT_SECRETS_FILE is
# # missing.
# MISSING_CLIENT_SECRETS_MESSAGE = """
# WARNING: Please configure OAuth 2.0

# To make this sample run you will need to populate the client_secrets.json file
# found at:

#    %s

# with information from the API Console
# https://console.cloud.google.com/

# For more information about the client_secrets.json file format, please visit:
# https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
# """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
#                                    CLIENT_SECRETS_FILE))

# VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# VIDEO_FILE_PATH = "facts.mp4"  # Replace with your video file path
# VIDEO_TITLE = "Did you know?"
# VIDEO_DESCRIPTION = "Did you know? " + fact
# VIDEO_CATEGORY = "27"  # Example category ID
# VIDEO_KEYWORDS = "Fun, Fact"  # Comma-separated keywords
# VIDEO_PRIVACY_STATUS = "public"  # Choose from "public", "private", "unlisted"


# def get_authenticated_service():
#   flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
#     scope=YOUTUBE_UPLOAD_SCOPE,
#     message=MISSING_CLIENT_SECRETS_MESSAGE)

#   storage = Storage("%s-oauth2.json" % sys.argv[0])
#   credentials = storage.get()

#   if credentials is None or credentials.invalid:
#     credentials = run_flow(flow, storage)

#   return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#     http=credentials.authorize(httplib2.Http()))

# def initialize_upload(youtube):
#   tags = None
#   if VIDEO_KEYWORDS:
#     tags = VIDEO_KEYWORDS.split(",")

#   body=dict(
#     snippet=dict(
#       title=VIDEO_TITLE,
#       description=VIDEO_DESCRIPTION,
#       tags=tags,
#       categoryId=VIDEO_CATEGORY
#     ),
#     status=dict(
#       privacyStatus=VIDEO_PRIVACY_STATUS
#     )
#   )

#   # Call the API's videos.insert method to create and upload the video.
#   insert_request = youtube.videos().insert(
#     part=",".join(body.keys()),
#     body=body,
#     # The chunksize parameter specifies the size of each chunk of data, in
#     # bytes, that will be uploaded at a time. Set a higher value for
#     # reliable connections as fewer chunks lead to faster uploads. Set a lower
#     # value for better recovery on less reliable connections.
#     #
#     # Setting "chunksize" equal to -1 in the code below means that the entire
#     # file will be uploaded in a single HTTP request. (If the upload fails,
#     # it will still be retried where it left off.) This is usually a best
#     # practice, but if you're using Python older than 2.6 or if you're
#     # running on App Engine, you should set the chunksize to something like
#     # 1024 * 1024 (1 megabyte).
#     media_body=MediaFileUpload(VIDEO_FILE_PATH, chunksize=-1, resumable=True)
#   )

#   resumable_upload(insert_request)

# # This method implements an exponential backoff strategy to resume a
# # failed upload.
# def resumable_upload(insert_request):
#   response = None
#   error = None
#   retry = 0
#   while response is None:
#     try:
#       print("Uploading file...")
#       status, response = insert_request.next_chunk()
#       if response is not None:
#         if 'id' in response:
#           print("Video id '%s' was successfully uploaded." % response['id'])
#         else:
#           exit("The upload failed with an unexpected response: %s" % response)
#     except HttpError as e:
#       if e.resp.status in RETRIABLE_STATUS_CODES:
#         error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
#                                                              e.content)
#       else:
#         raise
#     except RETRIABLE_EXCEPTIONS as e:
#       error = "A retriable error occurred: %s" % e

#     if error is not None:
#       print(error)
#       retry += 1
#       if retry > MAX_RETRIES:
#         exit("No longer attempting to retry.")

#       max_sleep = 2 ** retry
#       sleep_seconds = random.random() * max_sleep
#       print("Sleeping %f seconds and then retrying..." % sleep_seconds)
#       time.sleep(sleep_seconds)

# if __name__ == '__main__':  
#   if not os.path.exists(VIDEO_FILE_PATH):
#     exit("Please specify a valid file using the --file= parameter.")

#   youtube = get_authenticated_service()
#   try:
#     initialize_upload(youtube)
#   except HttpError as e:
#     print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

