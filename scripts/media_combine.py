from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
# sys.path.append('..')
import warnings
warnings.filterwarnings('ignore')

from utils.progress import progress_bar
from utils.scanfile import is_file


def media_combine(IN_FILE_AUDIO, IN_FILE_VIDEO, OUT_FILE, ffmpeg_location):
    if is_file(IN_FILE_AUDIO) and is_file(IN_FILE_VIDEO):
        result = ''
        try:
            audio_duration = float(ffmpeg.probe(IN_FILE_VIDEO)['format']['duration'])
            video_duration = float(ffmpeg.probe(IN_FILE_VIDEO)['format']['duration'])
            total_duration = min(audio_duration, video_duration)
            audio = ffmpeg.input(IN_FILE_AUDIO)
            video = ffmpeg.input(IN_FILE_VIDEO)
            result = progress_bar(
                (
                    ffmpeg
                    .output(audio.audio, video.video, f'{OUT_FILE}.mkv', acodec='copy', vcodec='copy', shortest=None)
                    .global_args('-progress', 'pipe:1', '-loglevel', 'error')
                    .overwrite_output()
                    .run_async(pipe_stdout=True, pipe_stderr=True, cmd=ffmpeg_location)
                ), total_duration, True)
        except ffmpeg.Error:
            sys.stdout.write('FFmpeg error, perhaps the file cannot be found\n')
            sys.exit(1)
        finally:
            sys.stdout.write(result)
            sys.exit(0)
    else:
        sys.stdout.write('Invalid input file format\n')
        sys.exit(0)


if __name__ == '__main__':
    # Required Arguments
    parser = argparse.ArgumentParser(description='Merge audio and video')
    parser.add_argument('IN_FILE_AUDIO', type=str, help='Input audio filename')
    parser.add_argument('IN_FILE_VIDEO', type=str, help='Input video filename')
    parser.add_argument('OUT_FILE', type=str, help='Output filename')

    # Optional Arguments
    parser.add_argument('-l', '--ffmpeg_location', type=str, default='ffmpeg.exe', help='FFmpeg location')

    args = parser.parse_args()
    
    if not args.IN_FILE_AUDIO or not args.IN_FILE_VIDEO or not args.OUT_FILE:
        sys.stdout.write('No file provided through IN_FILE_AUDIO, IN_FILE_VIDEO, or OUT_FILE')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        media_combine(args.IN_FILE_AUDIO, args.IN_FILE_VIDEO, args.OUT_FILE, args.ffmpeg_location)
