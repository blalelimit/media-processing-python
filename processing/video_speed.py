from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Generate sped up video')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-f', '--factor', type=float, default=1.2, help='Speed factor')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def speed_up_media(in_file, out_file, factor, ffmpeg_location):
    try:
        (
            ffmpeg
            .input(in_file)
            .output(f'{out_file}.mp4', filter_complex=f'atempo={factor};setpts=PTS*1/{factor}', vcodec='libx264', acodec='aac')
            .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    speed_up_media(args.in_file, args.out_file, args.factor, args.ffmpeg_location)