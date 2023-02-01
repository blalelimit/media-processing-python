#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Generate video thumbnail')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-t', '--time', type=float, default=0.5, help='Time offset')
parser.add_argument('-w', '--width', type=int, default=960,
    help='Width of output thumbnail (default 960, height automatically determined by aspect ratio)')


def generate_thumbnail(in_file, out_file, time, width):
    try:
        (
            ffmpeg
            .input(in_file, ss=time)
            .filter('scale', width, -1)
            .output(f'{out_file}.jpg', vframes=1, **{'qscale:v': 2})
            .run(overwrite_output=True, cmd='../ffmpeg/ffmpeg.exe', capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    generate_thumbnail(args.in_file, args.out_file, args.time, args.width)