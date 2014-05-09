
from pyqtmeta.meta import Helper
import os
import json
import argparse
import re


class Config(object):
    
    def __init__(self, d):
        self.tv_folder = None if not "tv_folder" in d else d["tv_folder"]
        self.movie_folder = None if not "movie_folder" in d else d["movie_folder"]
        self.tv_shows = None if not "tv_shows" in d else d['tv_shows']

    @staticmethod
    def from_config_file(path_to_config_file):
        if os.path.exists(path_to_config_file):
            with open(path_to_config_file, "r") as fp:
                file_text = fp.read()
                d = json.loads(file_text)
                return Config(d)
        return None


class Logic(object):

    @staticmethod
    def get_trailing_number(a_string):
        m = re.search(r'\d+$', a_string)
        return int(m.group()) if m else None

    @staticmethod
    def get_destination_folder_for_show(dest_folder, info):
        if dest_folder is None or info is None:
            return None
        show_path = os.path.join(dest_folder, info['show'])

        if not os.path.exists(show_path):
            return dest_folder
        
        season_folders = os.listdir(show_path)
        show_season_folder = None
        for a_folder in season_folders:
            a_number = Logic.get_trailing_number(a_folder)
            if a_number is not None and a_number == int(info['season_number']):
                show_season_folder = a_folder
                break
        if show_season_folder is not None:
            dest_folder = os.path.join(show_path, show_season_folder)
        return dest_folder

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="the path to the video file")
parser.add_argument("-c", "--config", help="the path to the config file (if none supplied it will expect it at ~/.itunes-helper.conf")
parser.add_argument("-i", "--info", default=False, help="show the meta data that can be derived from this video file", action='store_true')
parser.add_argument("-k", "--kind", default=None, help="let the script know what kind of video file it is (tv_show / movie)")
args = parser.parse_args()

movie_path = args.file_name
config_path = args.config
should_show_info_only = args.info
kind = args.kind

if config_path is None:
    config_path = os.path.expanduser("~/.itunes-helper.conf")
config = Config.from_config_file(config_path)

if config is None:
    d1 = {"tv_folder": "~/Movies/Series", "movie_folder": "~/Movies"}
    d2 = {"tv_folder": "/Volumes/Terra/movies/series", "movie_folder": "/Volumes/Terra/movies"}
    exit("Config is missing, a sample .itunes-helper.conf looks like this:\n%s\nor\n%s" % (json.dumps(d1), json.dumps(d2)))

if kind is None:
    i = raw_input("What kind of video file is %s?\nTV Show: 0\nMovie: 1\n> " % (os.path.basename(movie_path)))
    if i == '0':
        kind = 'tv_show'
    elif i == '1':
        kind = 'movie'

h = Helper()
destination_folder = None
meta_data = None
if kind == 'tv_show':
    meta_data = h.infer_metadata_from_tvshow_file(movie_path)
    if Helper.Keys.TVShow in meta_data and config.tv_shows is not None:
        title = meta_data[Helper.Keys.TVShow]
        title = title.lower()
        if title in config.tv_shows:
            meta_data[Helper.Keys.TVShow] = config.tv_shows[title]
    destination_folder = config.tv_folder
    destination_folder = Logic.get_destination_folder_for_show(destination_folder, meta_data)
elif kind == 'movie':
    meta_data = h.infer_metadata_from_movie_file(movie_path)
    destination_folder = config.movie_folder

if meta_data is None or len(meta_data) == 0:
    exit("Found no meta data")

if should_show_info_only:
    s = "Destination %s\nMeta data %s" % (destination_folder, str(meta_data))
    exit(s)

name = os.path.basename(movie_path)
destination_path = os.path.join(destination_folder, name)
h.set_metadata_with_dict(movie_path, meta_data, destination_path)

print "Updated %s with meta data %s" % (destination_path, str(meta_data))
