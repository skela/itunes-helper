
from pyqtmeta.meta import Helper
import os
import json
import argparse


class Config(object):
    
    def __init__(self, d):
        self.tv_folder = None if not "tv_folder" in d else d["tv_folder"]
        self.movie_folder = None if not "movie_folder" in d else d["movie_folder"]

    @staticmethod
    def from_config_file(path_to_config_file):
        if os.path.exists(path_to_config_file):
            with open(path_to_config_file, "r") as fp:
                s = fp.read()
                d = json.loads(s)
                return Config(d)
        return None

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="the path to the video file")
parser.add_argument("-c", "--config", help="the path to the config file (if none supplied it will expect it at ~/.itunes-helper.conf")
args = parser.parse_args()

movie_path = args.file_name
config_path = args.config

if config_path is None:
    config_path = os.path.expanduser("~/.itunes-helper.conf")
config = Config.from_config_file(config_path)

if config is None:
    d1 = {"tv_folder": "~/Movies/Series", "movie_folder": "~/Movies"}
    d2 = {"tv_folder": "/Volumes/Terra/movies/series", "movie_folder": "/Volumes/Terra/movies"}
    exit("Config is missing, a sample .itunes-helper.conf looks like this:\n%s\nor\n%s" % (json.dumps(d1), json.dumps(d2)))

h = Helper()

i = raw_input("What kind of video file is %s?\nTV Show: 0\nMovie: 1\n> " % (os.path.basename(movie_path)))

destination_folder = None
meta_data = None
if i == '0':
    meta_data = h.infer_metadata_from_tvshow_file(movie_path)
    destination_folder = config.tv_folder
elif i == '1':
    meta_data = h.infer_metadata_from_movie_file(movie_path)
    destination_folder = config.movie_folder

if meta_data is None or len(meta_data) == 0:
    exit("Found no meta data")

name = os.path.basename(movie_path)
destination_path = os.path.join(destination_folder, name)
h.set_metadata_with_dict(movie_path, meta_data, destination_path)

print "Updated %s with meta data %s" % (destination_path, str(meta_data))
