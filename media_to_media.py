from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
sys.path.append('..')
import warnings
warnings.filterwarnings('ignore')

from utils.progress import progress_bar
from utils.scanfile import is_file


class MediaConvert:
    def __init__(self, in_file, out_file, mformat, ffmpeg_location):
        self.in_file = in_file
        self.out_file = out_file
        self.mformat = mformat
        self.ffmpeg_location = ffmpeg_location

    def audio_convert(self):
        if is_file(self.in_file):
            result = ''
            try:
                total_duration = float(ffmpeg.probe(self.in_file)['format']['duration'])
                result = progress_bar(
                    (
                        ffmpeg
                        .input(self.in_file).audio
                        .output(f'{self.out_file}.{self.mformat}')
                        .global_args('-progress', 'pipe:1')
                        .overwrite_output()
                        .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                    ), total_duration, True)
            except ffmpeg.Error:
                sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is incorrect\n')
                sys.exit(1)
            finally:
                sys.stdout.write(result)
                sys.exit(1)
        else:
            sys.stdout.write('Invalid input file format\n')
            sys.exit(0)


    def video_convert(self):
        if is_file(self.in_file):
            result = ''
            try:
                out_files = self.out_file.split('.')
                total_duration = float(ffmpeg.probe(self.in_file)['format']['duration'])
                if out_files[-1].lower() == 'gif':
                    result = progress_bar(
                        (
                            ffmpeg
                            .input(self.in_file)
                            .output(f'{out_files[0]}.gif', ss=0, t=3, vf=f'fps=30,scale=960:-1:flags=lanczos', loop=0)
                            .global_args('-progress', 'pipe:1')
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                        ), total_duration)
                elif out_files[-1].lower() in ['mp4', 'mkv', 'avi', 'mov']:
                    result = progress_bar(
                        (
                            ffmpeg
                            .input(self.in_file)
                            .output(f'{self.out_file}.{self.format}')
                            .global_args('-progress', 'pipe:1')
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                        ), total_duration, True)
                else:
                    sys.stdout.write('Incorrect file format\n')
                    sys.exit(1)
            except ffmpeg.Error:
                sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is incorrect\n')
                sys.exit(1)
            finally:
                sys.stdout.write(result)
                sys.exit(0)
        else:
            sys.stdout.write('Invalid input file format\n')
            sys.exit(0)


if __name__ == '__main__':
    media_formats = ['mp3', 'ogg', 'opus', 'aac', 'm4a', 'flac', 'wav', 'gif', 'mp4', 'mkv', 'avi', 'mov']

    # Required Arguments
    parser = argparse.ArgumentParser(description='Convert media files')
    parser.add_argument('IN_FILE', type=str, help='Input filename')
    parser.add_argument('OUT_FILE', type=str, help='Output filename')
    parser.add_argument('MEDIA', choices=['a', 'v', 'b'], type=str, help='audio [a], video [v], or both [b]')
    parser.add_argument('FORMAT', choices=media_formats, type=str, help='''Audio or Video format types,
                        Audio Formats [mp3, ogg, opus, aac, m4a, flac, wav],
                        Video Formats [gif, mp4, mkv, avi, mov]''')
    
    # Optional Arguments
    parser.add_argument('-l', '--ffmpeg_location', type=str, default='ffmpeg.exe', help='FFmpeg location')

    args = parser.parse_args()

    if not args.IN_FILE or not args.OUT_FILE:
        sys.stdout.write('No file provided through IN_FILE or OUT_FILE')
        sys.stdout.write('\nType -h or --help for usage\n')
    elif not args.MEDIA:
        sys.stdout.write('Media type not provided through MEDIA')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        if args.MEDIA == 'a' and args.FORMAT.lower() in ['mp3', 'ogg', 'opus', 'aac', 'm4a', 'flac', 'wav']:
            MediaConvert(args.IN_FILE, args.OUT_FILE, args.FORMAT, args.ffmpeg_location).audio_convert()
        elif args.MEDIA == 'v' and args.FORMAT.lower() in ['gif', 'mp4', 'mkv', 'avi', 'mov']:
            MediaConvert(args.IN_FILE, args.OUT_FILE, args.FORMAT, args.ffmpeg_location).video_convert()
        else:
            sys.stdout.write('File format not valid')
            sys.stdout.write('\nType -h or --help for usage\n')