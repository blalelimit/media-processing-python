from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Generate sped up video')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-q', '--quality', default='a', help='Quality [High (h), Average (a), or Low (l)]')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def video_quality(in_file, out_file, quality, ffmpeg_location):
    if quality == 'h':
        crf = 17
    elif quality == 'l':
        crf = 51
    else:
        crf = 28
    try:
        (
            ffmpeg
            .input(in_file)
            .output(out_file, vcodec='libx265', crf=crf, preset='fast', acodec='aac', **{'b:a': '128k'})
            .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    video_quality(args.in_file, args.out_file, args.quality, args.ffmpeg_location)