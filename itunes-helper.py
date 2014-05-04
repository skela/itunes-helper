
from pyqtmeta.meta import Helper
import os
import sys

if not len(sys.argv) == 2:
    exit("Missing filename parameter. Syntax should be:\nitunes-helper.py file-name")
else:
    t = sys.argv[1]

movie_path = t

# with open(movie_path, 'rb') as fp:
#     movie = fp.read()
#     movie = open(movie_path, 'rb').read()
#     movie_atoms = AtomTree(movie)
#     meta_atom = movie_atoms.getAtomByPath(AtomPaths.meta)
#     show_atom = movie_atoms.getAtomByPath(AtomPaths.video_episode)
#     print movie_atoms.printTree()
#     print meta_atom.data
#     print show_atom

h = Helper()

i = raw_input("What kind of video file is %s?\nTV Show: 0\nMovie: 1\n> " % (os.path.basename(movie_path)))

destination_folder = None
meta_data = None
if i == '0':
    meta_data = h.infer_metadata_from_tvshow_file(movie_path)
    destination_folder = "/Volumes/Terra/movies/series"
elif i == '1':
    meta_data = h.infer_metadata_from_movie_file(movie_path)
    destination_folder = "/Volumes/Terra/movies"

if meta_data is None or len(meta_data) == 0:
    exit("Found no meta data")

name = os.path.basename(movie_path)
destination_path = os.path.join(destination_folder, name)
h.set_metadata_with_dict(movie_path, meta_data, destination_path)

print "Updated %s with meta data %s" % (destination_path, str(meta_data))
