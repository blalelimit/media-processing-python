#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import warnings
warnings.filterwarnings('ignore')
import sys


parser = argparse.ArgumentParser(description='Generate video thumbnail')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-t', '--time', type=float, default=0, help='Time offset')
parser.add_argument('-w', '--width', type=int, default=960,
    help='Width of output thumbnail (default 960, height automatically determined by aspect ratio)')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def generate_thumbnail(in_file, out_file, time, width, ffmpeg_location):
    try:
        total_duration = float(ffmpeg.probe(in_file)['format']['duration'])
        if time < 0 or time > total_duration:
            time = 0
        (
            ffmpeg
            .input(in_file, ss=time)
            .filter('scale', width, -1)
            .output(f'{out_file}.jpg', vframes=1, **{'qscale:v': 2})
            .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error:
        sys.stdout.write('FFmpeg error, perhaps the file cannot be found or input is incorrect.\n')
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.in_file or not args.out_file:
        sys.stdout.write('No file provided through --in_file or --out_file')
        sys.stdout.write('\nType -h or --help for usage')
    elif not args.time:
        sys.stdout.write('Time was not provided through --in_file or --out_file')
        sys.stdout.write('\nType -h or --help for usage')
    else:
        generate_thumbnail(args.in_file, args.out_file, args.time, args.width, args.ffmpeg_location)