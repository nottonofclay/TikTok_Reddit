import json
import requests
import os
from moviepy.editor import VideoFileClip,TextClip,CompositeVideoClip,concatenate_videoclips,AudioFileClip
from moviepy.video.tools.segmenting import findObjects
from random import randint
import pyttsx3


engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+20)

engine.setProperty('voice', voices[1].id)
os.chdir('C:\\Users\\tonof\\Documents\\Code\\Tiktok_Reddit\\Audiofiles')


def get_reddit(subreddit,listing,limit,timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

if __name__ == '__main__':
    data = get_reddit('AmItheAsshole','top','1','week')
    # with open('top.json') as f:
    #     data = json.load(f)

    for post in data['data']['children']:                                       # get the titles and posts
        title = post['data']['title']
        print('---------------------------------')
        text = post['data']['selftext']
        break

    reading_text = [title]
    counter = 0
    while len(text) > 0:
        if (text[counter] == '.'):
            reading_text.append(text[:counter+1])
            text = text[counter+1:]
            counter = 0
        else:
            counter += 1

    writing_text = []
    for i in reading_text:
        temp_str = ''
        split_str = ''
        for j in i.split():
            if len(temp_str + j) < 25:
                temp_str += j + ' '
            else:
                split_str += temp_str + '\n'
                temp_str = j + ' '
        writing_text.append(split_str + temp_str)

    x = randint(0,5)
    final_clip = VideoFileClip('parkour.mp4').subclip(0,0.00001).without_audio()

    for i in range(len(reading_text)):             # change to len(revised_text) in final, 10 is here for speed during testing
        engine.save_to_file(reading_text[i], 'audio' + str(i) + '.mp3')
        engine.runAndWait()
        audio = AudioFileClip('audio' + str(i) + '.mp3')
        audio = audio.subclip(0,audio.duration)

        length = audio.duration
        video = VideoFileClip('parkour.mp4').subclip(x,x+length).without_audio()
        if (i==0):
            font_size = 40
        else:
            font_size = 20
        txt_clip = (TextClip(' '.join(writing_text[i]),fontsize=40,color='white',font='Comic-Sans-MS',kerning=-6.5)   # 25 chars
                .set_position('center')
                .set_duration(length) )

        result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
        result = result.set_audio(audio)

        final_clip = concatenate_videoclips([final_clip,result]) # Many options...
        x += length

    os.chdir('C:\\Users\\tonof\\Documents\\Code\\Tiktok_Reddit')

    final_clip.write_videofile('parkour_edited.mp4')