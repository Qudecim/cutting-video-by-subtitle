import os

r_dir = 'video'

list_movies = os.listdir(path="./resource/" + r_dir + "/")
for movie in list_movies:
    dir_movie = "./resource/" + r_dir + "/" + movie
    list_seasons = os.listdir(path=dir_movie)
    for season in list_seasons:
        dir_season = "./resource/" + r_dir + "/" + movie + "/" + season
        list_parts = os.listdir(path=dir_season)
        list_parts.sort()
        for index, part in enumerate(list_parts):
            dir_part = "./resource/" + r_dir + "/" + movie + "/" + season + "/"
            file = index + 1
            file_name = str(file)
            if file < 10:
                file_name = "0" + str(file)
            extension = part.split('.')[1]
            os.rename(dir_part + part, dir_part + file_name + "." + extension)
