from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys


parser = argparse.ArgumentParser(description='Merge audio and video')
parser.add_argument('-a', '--in_file_audio', help='Input audio filename')
parser.add_argument('-v', '--in_file_video', help='Input video filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-l', '--ffmpeg_location', default='ffmpeg.exe', help='FFmpeg location')


def media_merge(in_file_audio, in_file_video, out_file, ffmpeg_location):
    try:
        audio = ffmpeg.input(in_file_audio)
        video = ffmpeg.input(in_file_video)
        (
            ffmpeg
            .output(audio.audio, video.video, out_file, acodec='aac', shortest=None, vcodec='copy')
            .run(overwrite_output=True, cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    args = parser.parse_args()
    media_merge(args.in_file_audio, args.in_file_video, args.out_file, args.ffmpeg_location)
