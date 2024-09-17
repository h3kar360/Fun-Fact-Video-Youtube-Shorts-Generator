from moviepy.editor import *
from moviepy.config import change_settings
import requests
from gtts import gTTS

IMAGEMAGICK_PATH = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_PATH})

def findLenFact():
    api_url = 'https://api.api-ninjas.com/v1/facts'
    response = requests.get(api_url, headers={'X-Api-Key': 'A58p2qySrkVl5IevVv9iUw==DEQRx34va7nznCTl'})
    if response.status_code == requests.codes.ok:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)

    fact = data[0]["fact"]   

    if len(fact) >= 10:
        splitStr = fact.split(' ')
        newSplit = []
        for i in range(0, len(splitStr)):
            newSplit.append(splitStr[i])
            if (i+1)%4 == 0:
                newSplit.append('\n')
    
        combinedSplit = ' '.join(newSplit)
        return combinedSplit
    else:
        return findLenFact()
    
fact = findLenFact()
print(fact)
speech = 'fun fact, ' + fact

convertTS = gTTS(text=speech, lang='en-uk', slow=False)

convertTS.save('audio/randFacts.mp3')

def get_background():
    client_id = 'Ko4iF-DnABl-jHt3SsLr96hE-IQXhNoyyKHPxrVkJx4'
    query = 'nature'
    url = f'https://api.unsplash.com/photos/random/?client_id={client_id}&query={query}&orientation=portrait'

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

audio = AudioFileClip('audio/randFacts.mp3')

duration = audio.duration

bgMusic = AudioFileClip('audio/fsm-team-escp-autumn-dance.mp3').volumex(0.2).set_duration(duration);

combAud = CompositeAudioClip([audio, bgMusic])

background = ImageClip('background/background.png').set_duration(duration)

text = TextClip(fact, fontsize=50, color='black', font='Arial-Bold', stroke_color='white', stroke_width=2).set_position('center').set_duration(duration).crossfadein(1)    

background = background.set_audio(combAud)

video = CompositeVideoClip([background, text])

video.write_videofile('facts.mp4', fps=24)