from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import warnings
warnings.filterwarnings('ignore')
import sys
# sys.path.append('..')

from utils.progress import progress_bar
from utils.checkfile import check_file


parser = argparse.ArgumentParser(description='Convert media files')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-m', '--media', help='''Audio [a] or Video [v] media,
                    Audio Formats [mp3, ogg, opus, m4a, flac, wav],
                    Video Formats [gif, mp4, mkv, avi, mov]''')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


class AVConvert:
    def __init__(self, in_file, out_file, ffmpeg_location):
        self.in_file = in_file
        self.out_file = out_file
        self.ffmpeg_location = ffmpeg_location

    def audio_convert(self):
        if check_file(self.in_file):
            result = ''
            try:
                total_duration = float(ffmpeg.probe(self.in_file)['format']['duration'])
                if self.out_file.split('.')[-1] in ['mp3', 'ogg', 'opus', 'm4a', 'flac', 'wav']:
                    result = progress_bar(
                        (
                            ffmpeg
                            .input(self.in_file).audio
                            .output(f'{self.out_file}')
                            .global_args('-progress', 'pipe:1')
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                        ), total_duration)
                else:
                    print('Incorrect file format')
                    sys.exit(1)
            except ffmpeg.Error:
                sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is incorrect.\n')
                sys.exit(1)
            finally:
                sys.stdout.write(result)
                sys.exit(1)
        else:
            sys.stdout.write('Invalid input file format.\n')
            sys.exit(0)


    def video_convert(self):
        if check_file(self.in_file):
            result = ''
            try:
                out_files = self.out_file.split('.')
                total_duration = float(ffmpeg.probe(self.in_file)['format']['duration'])
                if out_files[-1] == 'gif':
                    result = progress_bar(
                        (
                            ffmpeg
                            .input(self.in_file)
                            .output(f'{out_files[0]}.gif', ss=0, t=3, vf=f'fps=30,scale=960:-1:flags=lanczos', loop=0)
                            .global_args('-progress', 'pipe:1')
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                        ), total_duration)
                elif out_files[-1] in ['mp4', 'mkv', 'avi', 'mov']:
                    result = progress_bar(
                        (
                            ffmpeg
                            .input(self.in_file)
                            .output(f'{self.out_file}')
                            .global_args('-progress', 'pipe:1')
                            .overwrite_output()
                            .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                        ), total_duration)
                else:
                    print('Incorrect file format')
                    sys.exit(1)
            except ffmpeg.Error:
                sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is incorrect.\n')
                sys.exit(1)
            finally:
                sys.stdout.write(result)
                sys.exit(1)
        else:
            sys.stdout.write('Invalid input file format.\n')
            sys.exit(0)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.in_file or not args.out_file:
        sys.stdout.write('No file provided through --in_file or --out_file')
        sys.stdout.write('\nType -h or --help for usage\n')
    if not args.media:
        sys.stdout.write('Media not provided through -m or --media')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        if args.media == 'a':
            AVConvert(args.in_file, args.out_file, args.ffmpeg_location).audio_convert()
        elif args.media == 'v':
            AVConvert(args.in_file, args.out_file, args.ffmpeg_location).video_convert()
        else:
            sys.stdout.write('Media type not valid. Accepted inputs (a or b)')
            sys.stdout.write('\nType -h or --help for usage\n')