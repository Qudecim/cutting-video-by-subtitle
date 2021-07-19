import os

resource_path = '/media/hackpsy/005EADA65EAD94C6/clips/'
r_dir = 'video'

list_movies = os.listdir(path=resource_path + r_dir + "/")
for movie in list_movies:
    if movie[0] == '_':
        continue
    dir_movie = resource_path + r_dir + "/" + movie
    list_seasons = os.listdir(path=dir_movie)
    for season in list_seasons:
        dir_season = resource_path + r_dir + "/" + movie + "/" + season
        list_parts = os.listdir(path=dir_season)
        list_parts.sort()
        for index, part in enumerate(list_parts):
            dir_part = resource_path + r_dir + "/" + movie + "/" + season + "/"
            file = index + 1
            file_name = str(file)
            if file < 10:
                file_name = "0" + str(file)
            extension = part.split('.')[-1]
            os.rename(dir_part + part, dir_part + file_name + "." + extension)
