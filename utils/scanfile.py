import sys
import ffmpeg
from os.path import isfile


# Checks if the path is a file
def is_file(path):
    return isfile(path)


# Checks if file is an audio or video, checks if audio has attached picture
def probe_file(file):
    try:
        stream_list = list()
        is_image = 0
        probed = ffmpeg.probe(file)
        for stream in probed['streams']:
            stream_list.append(stream['codec_type'])
            is_image = stream['disposition']['attached_pic']
        return set(['audio']) if is_image else set(stream_list) 
    except ffmpeg.Error as e:
        sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is not valid\n') # e.stderr.decode())
        sys.exit(1)


# Gets video width and height
def get_video_dimensions(file):
    try:
        probed = ffmpeg.probe(file)
        for stream in probed['streams']:
            if 'width' in stream:
                return [stream['width'], stream['height']]
        return list()
    except ffmpeg.Error:
        sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is not valid\n') # e.stderr.decode())
        sys.exit(1)
        

