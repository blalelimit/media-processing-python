from __future__ import unicode_literals, print_function

import argparse
import ffmpeg
import warnings
warnings.filterwarnings('ignore')
import sys
# sys.path.append('..')

from utils.progress import progress_bar
from utils.checkfile import check_file


parser = argparse.ArgumentParser(description='Merge audio and video')
parser.add_argument('-a', '--in_file_audio', help='Input audio filename')
parser.add_argument('-v', '--in_file_video', help='Input video filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def media_merge(in_file_audio, in_file_video, out_file, ffmpeg_location):
    result = ''
    if check_file(in_file_audio) and check_file(in_file_video):
        try:
            audio_duration = float(ffmpeg.probe(in_file_audio)['format']['duration'])
            video_duration = float(ffmpeg.probe(in_file_video)['format']['duration'])
            total_duration = min(audio_duration, video_duration)
            audio = ffmpeg.input(in_file_audio)
            video = ffmpeg.input(in_file_video)
            result = progress_bar(
                (
                    ffmpeg
                    .output(audio.audio, video.video, f'{out_file}.mp4', acodec='aac', shortest=None, vcodec='copy')
                    .global_args('-progress', 'pipe:1', '-loglevel', 'error')
                    .overwrite_output()
                    .run_async(pipe_stdout=True, pipe_stderr=True, cmd=ffmpeg_location)
                ), total_duration)
        except ffmpeg.Error:
            sys.stdout.write('FFmpeg error, perhaps the file cannot be found.\n')
            sys.exit(1)
        finally:
            sys.stdout.write(result)
            sys.exit(1)
    else:
        sys.stdout.write('Invalid input file format.\n')
        sys.exit(0)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.in_file_audio or not args.in_file_video or not args.out_file:
        sys.stdout.write('No file provided through --in_file_audio, --in_file_video or --out_file')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        media_merge(args.in_file_audio, args.in_file_video, args.out_file, args.ffmpeg_location)
