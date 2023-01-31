from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Convert media files')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-m', '--media', help='''Audio [a] or Video [v] Format,
                    Audio Formats [mp3, ogg, opus, m4a, flac, wav],
                    Video Formats [gif, mp4, mkv, avi, mov]''')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def audio_convert(in_file, out_file, ffmpeg_location):
    try:
        out_files = out_file.split('.')
        if out_files[len(out_files)-1] in ['mp3', 'ogg', 'opus', 'm4a', 'flac', 'wav']:
            (
                ffmpeg
                .input(in_file)
                .output(out_files[0].out_files[len(out_files)-1])
                .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
            )
        else:
            print('Incorrect file format')
            sys.exit(1)
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def video_convert(in_file, out_file, ffmpeg_location):
    try:
        out_files = out_file.split('.')
        if out_files[len(out_files)-1] == 'gif':
            (
                ffmpeg
                .input(in_file)
                .output(f'{out_files[0]}.gif', ss=0, t=3, vf=f'fps=30,scale=960:-1:flags=lanczos', loop=0)
                .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
            )
        elif out_files[len(out_files)-1] in ['mp4', 'mkv', 'avi', 'mov']:
            (
                ffmpeg
                .input(in_file)
                .output(out_files[0].out_files[len(out_files)-1])
                .run(overwrite_output=True, cmd='ffmpeg/ffmpeg.exe', capture_stdout=True, capture_stderr=True)
            )
        else:
            print('Incorrect file format')
            sys.exit(1)
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.media == 'a':
        audio_convert(args.in_file, args.out_file, args.ffmpeg_location)
    elif args.media == 'v':
        video_convert(args.in_file, args.out_file, args.ffmpeg_location)
    else:
        print('Type -h or --help for usage')
        sys.exit(1)