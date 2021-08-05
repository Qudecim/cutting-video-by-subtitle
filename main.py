import os
#from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
import hashlib
import mysql.connector
import time

resource_path = '/media/hackpsy/005EADA65EAD94C6/clips/'


def prepare_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def get_phrase():
    return open(resource_path + 'phrases/1.txt', 'r')


def get_sub(movie, season, part):
    return open(resource_path + 'subs/' + movie + '/' + season + '/' + part + '.srt', 'rb').readlines()


def get_time(file, line, iter = 0):
    n_iter = iter + 1
    if n_iter > 20:
        return False
    try:
        if line < 0:
            return get_pre_time(str(file[1], 'utf-8').rstrip())
        text = str(file[line - 1], 'utf-8').rstrip()
        if text == '':
            return get_pre_time(str(file[line + 1], 'utf-8').rstrip())
        return get_time(file, line - 1, n_iter)
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
    list_movies = os.listdir(path=resource_path + "subs/")
    for movie in list_movies:
        if movie[0] == '_':
            continue
        dir_movie = resource_path + "subs/" + movie
        list_seasons = os.listdir(path=dir_movie)
        for season in list_seasons:
            dir_season = resource_path + "subs/" + movie + "/" + season
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


def make_clip(data, phrase):
    ext = get_extension_video(data['movie'], data['season'], data['part'])
    if not ext:
        return
    o_phrase_hash = hashlib.md5(str(phrase).encode())
    phrase_hash = o_phrase_hash.hexdigest()
    prepare_dir(resource_path + 'out/' + phrase_hash)
    file_name = data['movie'] + '__' + data['season'] + '__' + data['part'] + '__' + str(data['time_start'])
    cut_video(resource_path + "video/" + data['movie'] + "/" + data['season'] + "/" + data['part'] + "." + ext,
              resource_path + "out/" + phrase_hash + "/" + file_name + ".mp4",
              data['time_start'], data['time_end'])


def cut_video(file_in, file_out, t1, t2):
    try:
        with VideoFileClip(file_in) as video:
            new = video.subclip(t1 - 1, t2 + 1)
            new.write_videofile(file_out, audio_codec='aac')
    except:
        return False
        #
        # new.write_videofile(file_out, fps=30, threads=1, codec="libx264")
        #
        # ffmpeg_extract_subclip(file_in,
        #                        t1, t2,
        #                        targetname=file_out)


def get_extension_video(movie, season, part):
    path = resource_path + "video/" + movie + "/" + season + "/" + part
    if os.path.exists(path + ".mp4"):
        return 'mp4'
    if os.path.exists(path + ".avi"):
        return 'avi'
    if os.path.exists(path + ".mkv"):
        return 'mkv'
    return False


class Phrase:

    db = 0

    def __init__(self):
        self.db = mysql.connector.connect(user='animania', password='123ZXCzxc', host='127.0.0.1', database='eng')
        self.index()

    def add(self, hash, movie, season, part, use, time_start, extension):
        params = [hash, movie, season, part, time_start, use, extension,
                  time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')]
        insert_movies_query = """
        INSERT INTO `clips_phrases`(`word_hash`, `movie`, `season`, `part`, `start_time`,
                                    `active`, `extension`, `created_at`, `updated_at`)
        VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        with self.db.cursor() as cursor:
            cursor.execute(insert_movies_query, params)
            self.db.commit()

    def index(self):
        with open('log.txt', 'a') as file:
            phrases = get_phrase()
            for phrase_line in phrases:
                a_phrases = phrase_line.split('|')
                phrase = a_phrases[0]
                cut_data = get_cut_data(phrase)
                o_phrase_hash = hashlib.md5(str(phrase).encode())
                phrase_hash = o_phrase_hash.hexdigest()
                file.write(phrase + ' ' + phrase_hash + '\n')
                for cut_data_item in cut_data:
                    make_clip(cut_data_item, phrase)
                    extension = get_extension_video(cut_data_item['movie'], cut_data_item['season'], cut_data_item['part'])
                    self.add(phrase_hash, cut_data_item['movie'], cut_data_item['season'], cut_data_item['part'], 1, cut_data_item['time_start'], extension)
                    file.write('-- movie:' + cut_data_item['movie'] +
                               ' season:' + cut_data_item['season'] +
                               ' part:' + cut_data_item['part'] + '\n'
                               )
                file.write('\n')


x = Phrase()
