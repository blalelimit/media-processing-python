from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Generate flipped video')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-f', '--flip', default='hflip', help='Flip video vertically [vflip] or horizontally [hflip]')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def flip_video(in_file, out_file, flip, ffmpeg_location):
    if flip not in ['hflip', 'vflip']:
        flip = 'hflip'
    try:
        (
            ffmpeg
            .input(in_file)
            .output(out_file, filter_complex=flip)
            .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    flip_video(args.in_file, args.out_file, args.flip, args.ffmpeg_location)