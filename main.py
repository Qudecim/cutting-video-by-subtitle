import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def get_phrase():
    return open('resource/phrases/1.txt')


def get_sub(movie, part):
    return open('resource/subs/' + movie + '/' + part + '.srt', 'r').readlines()


def get_time(file, line):
    if file[line - 1].rstrip() == '':
        return get_pre_time(file[line + 1].rstrip())
    return get_time(file, line - 1)


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
    print(list_time)
    h = int(list_time[0])
    m = int(list_time[1])
    s = int(list_time[2])
    return s + (m*60) + (h*60*60)


def get_cut_data(phrase):
    cut_data = []
    list_movies = os.listdir(path="./resource/subs/")
    for movie in list_movies:
        dir_movie = "./resource/subs/" + movie
        list_parts = os.listdir(path=dir_movie)
        for part in list_parts:
            part_id = part.split('.')[0]
            file_sub = get_sub(movie, part_id)
            for sub_line, sub_text in enumerate(file_sub):
                if phrase in sub_text:
                    time = get_time(file_sub, sub_line)
                    data = dict()
                    data['movie'] = movie
                    data['part'] = part_id
                    data['time_start'] = time['start']
                    data['time_end'] = time['end']
                    cut_data.append(data)
    return cut_data


def cut_video(data, phrase_index, index):
    ffmpeg_extract_subclip("./resource/video/" + data['movie'] + "/" + data['part'] + ".mp4",
                           data['time_start'], data['time_end'],
                           targetname="./resource/out/" + str(phrase_index) + "/" + str(index) + ".mp4")


class Phrase:

    def __init__(self):
        phrases = get_phrase()
        for phrase_index, phrase in enumerate(phrases):
            cut_data = get_cut_data(phrase)
            for index, cut_data_item in enumerate(cut_data):
                cut_video(cut_data_item, phrase_index, index)



x = Phrase()

# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# # ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
# ffmpeg_extract_subclip("1.mp4", 0, 20, targetname="cut.mp4")
