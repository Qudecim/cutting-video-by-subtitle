import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import re


def prepare_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def get_phrase():
    return open('resource/phrases/1.txt', 'r')


def get_sub(movie, season, part):
    return open('resource/subs/' + movie + '/' + season + '/' + part + '.srt', 'rb').readlines()


def get_time(file, line):
    try:
        if line < 0:
            return get_pre_time(str(file[1], 'utf-8').rstrip())
        print(file[line - 1])
        text = str(file[line - 1], 'utf-8').rstrip()
        if text == '':
            return get_pre_time(str(file[line + 1], 'utf-8').rstrip())
        return get_time(file, line - 1)
    except UnicodeDecodeError:
        return False


def get_pre_time(str_time):
    time = dict()
    str_time_ = str_time.replace(' ', '')
    list_time = str_time_.split('-->')
    time['start'] = str_to_time(list_time[0])
    time['end'] = str_to_time(list_time[1])
    return time


def str_to_time(time):
    time_ = time.split(',')
    time = time_[0]
    list_time = time.split(':')
    h = int(list_time[0])
    m = int(list_time[1])
    s = int(list_time[2])
    return s + (m * 60) + (h * 60 * 60)


def get_cut_data(phrase):
    cut_data = []
    list_movies = os.listdir(path="./resource/subs/")
    for movie in list_movies:
        dir_movie = "./resource/subs/" + movie
        list_seasons = os.listdir(path=dir_movie)
        for season in list_seasons:
            dir_season = "./resource/subs/" + movie + "/" + season
            list_parts = os.listdir(path=dir_season)
            for part in list_parts:
                part_id = part.split('.')[0]
                file_sub = get_sub(movie, season, part_id)
                for sub_line, sub_text in enumerate(file_sub):
                    good_phrase = phrase.rstrip()
                    if good_phrase in str(sub_text):
                        time = get_time(file_sub, sub_line)
                        if not time:
                            continue
                        data = dict()
                        data['movie'] = movie
                        data['season'] = season
                        data['part'] = part_id
                        data['time_start'] = time['start']
                        data['time_end'] = time['end']
                        cut_data.append(data)
    return cut_data


def make_clip(data, phrase_index, index):
    # print(data)
    # return
    cut_video("./resource/video/" + data['movie'] + "/" + data['season'] + "/" + data['part'] + ".avi",
              "./resource/out/" + str(phrase_index) + "/" + str(index) + ".mp4",
              data['time_start'], data['time_end'])


def cut_video(file_in, file_out, t1, t2):
    with VideoFileClip(file_in) as video:
        new = video.subclip(t1 - 1, t2 + 1)
        new.write_videofile(file_out, audio_codec='aac')
        #
        # new.write_videofile(file_out, fps=30, threads=1, codec="libx264")
        #
        # ffmpeg_extract_subclip(file_in,
        #                        t1, t2,
        #                        targetname=file_out)


class Phrase:

    def __init__(self):
        phrases = get_phrase()
        for phrase_index, phrase in enumerate(phrases):
            cut_data = get_cut_data(phrase)
            for index, cut_data_item in enumerate(cut_data):
                make_clip(cut_data_item, phrase_index, index)


x = Phrase()

# d = b"<i>It's my first day.</i>\r\n"
# f = "It's my first day."
# phrases = get_phrase()
# for phrase_index, phrase in enumerate(phrases):
#     dd = str(phrase).rstrip()
#     #dd = dd.replace("\n", "")
#     print(dd)
#     print(d)
#     print(str(dd) in str(d))
