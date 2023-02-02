from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import warnings
warnings.filterwarnings('ignore')
import sys
# sys.path.append('..')

from utils.progress import progress_bar
from utils.checkfile import check_file


parser = argparse.ArgumentParser(description='Generate sped up audio/video')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-m', '--media', type=str, help='audio [a], video [v], or both [b]')
parser.add_argument('-f', '--factor', type=float, default=1.2, help='Factor to speed up audio/video')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


class SpeedUp:
    def __init__(self, in_file, out_file, media, factor, ffmpeg_location):
        self.in_file = in_file
        self.out_file = out_file
        self.media_type = media
        self.factor = factor
        self.ffmpeg_location = ffmpeg_location

    def speed_up(self):
        if check_file(self.in_file):
            result = ''
            try:
                total_duration = float(ffmpeg.probe(self.in_file)['format']['duration'])
                if self.media == 'a':
                    kwargs = dict(filename=f'{self.out_file}.m4a', filter_complex=f'[0:a]atempo={self.factor}[a]', map='[a]', acodec='aac')
                elif self.media == 'v':
                    kwargs = dict(filename=f'{self.out_file}.mp4', filter_complex=f'[0:v]setpts=PTS*1/{self.factor}[v]', map='[v]', vcodec='libx264')
                elif self.media == 'b':
                    kwargs = dict(filename=f'{self.out_file}.mp4', filter_complex=f'atempo={self.factor};setpts=PTS*1/{self.factor}', vcodec='libx264', acodec='aac')
                process = (
                    ffmpeg
                    .input(self.in_file)
                    .output(**kwargs)
                    .global_args('-progress', 'pipe:1', '-loglevel', 'error')
                    .overwrite_output()
                    .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                )
                result = progress_bar(process, total_duration)
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
    if not args.in_file or not args.out_file:
        sys.stdout.write('No file provided through -i/--in_file or -o/--out_file')
        sys.stdout.write('\nType -h or --help for usage\n')
    elif not args.media:
        sys.stdout.write('Media type (a or v) not provided through -m or --media_type')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        if args.media not in ['a', 'v', 'b']:
            sys.stdout.write('Media type not valid. Accepted inputs (a, v, or b)')
            sys.stdout.write('\nType -h or --help for usage\n')
        else:
            SpeedUp(args.in_file, args.out_file, args.media, args.factor, args.ffmpeg_location).speed_up()
