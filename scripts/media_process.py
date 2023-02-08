from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
# sys.path.append('..')
import warnings
warnings.filterwarnings('ignore')

from utils.progress import progress_bar
from utils.scanfile import is_file, probe_file, get_video_dimensions


def check_additional_args(EFFECT, additional_args):
    if EFFECT == 't':
        if not additional_args.trim:
            sys.stdout.write('No inputs for trim given through -t or --trim\n')
            sys.exit(0)
        elif len(list(additional_args.trim.split(':'))) != 2:
            sys.stdout.write('Incorrect input format for trim, example input "0:10"\n')
            sys.exit(0)
    elif EFFECT == 'a' and not additional_args.add_file:
        sys.stdout.write('Additional input file not given through -a or --add_file\n')
        sys.exit(0)
    elif EFFECT == 'f' and not additional_args.factor:
        sys.stdout.write('No inputs for speed factor through -f or --factor\n')
        sys.exit(0)
    elif EFFECT == 's':
        if not additional_args.saturation and additional_args.saturation != 0:
            sys.stdout.write('No inputs for saturation through -s or --saturation\n')
            sys.exit(0)
        elif additional_args.saturation < -10 or additional_args.saturation > 10:
            sys.stdout.write('Incorrect input for hue saturation value, must be between -10 and 10, inclusive\n')
            sys.exit(0)
    elif EFFECT == 'd' and not additional_args.draw_text:
        sys.stdout.write('No input text given through -d or --draw_text\n')
        sys.exit(0)
    elif EFFECT == 'tb' and not additional_args.thumbnail and additional_args.thumbnail != 0:
        sys.stdout.write('No input text given through -tb or --thumbnail\n')
        sys.exit(0)


class AdditionalArgs:
    def __init__(self, trim, add_file, factor, saturation, draw_text, x_coord, y_coord, thumbnail):
        self.trim = trim
        self.add_file = add_file
        self.factor = factor
        self.saturation = saturation
        self.draw_text = draw_text
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.thumbnail = thumbnail


class VideoEffect:
    def __init__(self, IN_FILE, OUT_FILE, EFFECT, ffmpeg_location, additional_args):
        self.IN_FILE = IN_FILE
        self.OUT_FILE = OUT_FILE
        self.EFFECT = EFFECT
        self.ffmpeg_location = ffmpeg_location
        self.additional_args = additional_args
        
        
    def select_option(self):
        total_duration = float(ffmpeg.probe(self.IN_FILE)['format']['duration'])
        outputs = dict()
        global_args = {}

        # No additional args required
        if self.EFFECT in ['hflip', 'vflip', 'q']:
            # Flip video
            if self.EFFECT in ['hflip', 'vflip']:
                outputs = dict(filename=f'{self.OUT_FILE}.mp4', vcodec='libx264', filter_complex=self.EFFECT)
            # Lower video quality
            elif self.EFFECT == 'q':
                outputs = dict(filename=f'{self.OUT_FILE}.mp4', vcodec='libx264', crf=28, preset='fast')
        
        # Requires additional args
        elif self.EFFECT in ['t', 'a', 'f', 's', 'd', 'tb']: 
            check_additional_args(self.EFFECT, self.additional_args)
            # Trim video
            if self.EFFECT == 't':
                st, to = list(map(int, self.additional_args.trim.split(':')))      
                if st < 0 or to > total_duration:
                    sys.stdout.write('Invalid starting time or duration.\n')
                    sys.exit(0)
                else:
                    total_duration = to - st
                    streams_list = probe_file(self.IN_FILE)
                    if 'audio' in streams_list and 'video' in streams_list:
                        print('Audio and video codecs found')
                        outputs = dict(filename=f'{self.OUT_FILE}.mp4', codec='copy', ss=st, to=to) 
                    elif 'audio' in streams_list:
                        print('Audio codec found')
                        outputs = dict(filename=f'{self.OUT_FILE}.m4a', codec='copy', ss=st, to=to) 
                    elif 'video' in streams_list:
                        print('Video codec found')
                        outputs = dict(filename=f'{self.OUT_FILE}.mp4', codec='copy', ss=st, to=to) 

            # Concat video
            elif self.EFFECT == 'a':
                add_file = self.additional_args.add_file
                streams_list_a = probe_file(self.IN_FILE)
                streams_list_b = probe_file(add_file)

                # Check codecs in files and are same
                same_codec = list(streams_list_a.intersection(streams_list_b))
                if len(same_codec) == 2:
                    print('Audio and video codecs found')
                    outputs = dict(filename=f'{self.OUT_FILE}.mkv', vcodec='libx264', map='[v]', preset='fast',
                        filter_complex="[0:v]scale=1280x720,setdar=16/9[v0];[1:v]scale=1280x720,setdar=16/9[v1];[v0][v1]concat=n=2:v=1:a=0[v]")
                elif 'audio' in same_codec:
                    print('Audio codec found')
                    outputs = dict(filename=f'{self.OUT_FILE}.m4a', acodec='aac',
                        filter_complex='[0:a][1:a]concat=n=2:v=0:a=1[a]', map='[a]')
                elif 'video' in same_codec:
                    print('Video codec found')
                    outputs = dict(filename=f'{self.OUT_FILE}.mkv', vcodec='libx264', map='[v]', preset='fast',
                        filter_complex="[0:v]scale=1280x720,setdar=16/9[v0];[1:v]scale=1280x720,setdar=16/9[v1];[v0][v1]concat=n=2:v=1:a=0[v]")
                else:
                    print('Both inputs are not the same format')
                    exit(0)

                total_duration = float(ffmpeg.probe(self.IN_FILE)['format']['duration']) + float(
                            ffmpeg.probe(add_file)['format']['duration'])
                global_args = {'-i', add_file}

            # Speed up video based on factor
            elif self.EFFECT == 'f':
                streams_list = probe_file(self.IN_FILE)
                factor = self.additional_args.factor
                total_duration = float(ffmpeg.probe(self.IN_FILE)['format']['duration']) / factor

                # Check codecs in file
                if 'audio' in streams_list and 'video' in streams_list:
                    print('Audio and video codecs found')
                    outputs = dict(filename=f'{self.OUT_FILE}.mkv', filter_complex=f'atempo={factor};setpts=PTS*1/{factor}',
                            acodec='aac')
                elif 'audio' in streams_list:
                    print('Audio codec found')
                    outputs = dict(filename=f'{self.OUT_FILE}.m4a', filter_complex=f'[0:a]atempo={factor}[a]',
                            map='[a]', acodec='aac')
                elif 'video' in streams_list:
                    print('Video codec found')
                    outputs = dict(filename=f'{self.OUT_FILE}.mkv', filter_complex=f'[0:v]setpts=PTS*1/{factor}[v]',
                            map='[v]', vcodec='libx264')

            # Change video hue saturation
            elif self.EFFECT == 's':
                value = self.additional_args.saturation
                outputs = dict(filename=f'{self.OUT_FILE}.mkv', vcodec='libx264', filter_complex=f'hue=s={value}', preset='fast')
                
            # Draw text on video
            elif self.EFFECT == 'd':
                text = self.additional_args.draw_text
                x =  self.additional_args.x_coord
                y =  self.additional_args.y_coord
                outputs = dict(filename=f'{self.OUT_FILE}.mkv', vcodec='libx264',
                    filter_complex=f'drawtext=text={text}:x={x}:y={y}:fontsize=35:fontcolor=white')

            # Generate thumbnail as *.jpg image
            elif self.EFFECT == 'tb':
                streams_list = probe_file(self.IN_FILE)
                time = self.additional_args.thumbnail
                if 'video' in streams_list:
                    if time < 0 or time > total_duration:
                        print('Offset time is not within the video bounds')
                        exit(0)
                    else:
                        total_duration = 1
                        width, height = get_video_dimensions(self.IN_FILE)
                        outputs = dict(filename=f'{self.OUT_FILE}.jpg', vframes=1, ss=time,
                            **{'qscale:v': 2, 'filter:v' : f'scale={width}:{height}'})
                else:
                    print('No video codec found, invalid input')
                    exit(0)

        # Error handler
        else:
            sys.stdout.write('Invalid effect chosen')
            sys.stdout.write('\nType -h or --help for usage\n')
            sys.exit(0)

        return total_duration, outputs, global_args

    def video_effect(self):
        result = ''
        try:
            total_duration, outputs, global_args = self.select_option()
            result = progress_bar(
                (
                    ffmpeg
                    .input(self.IN_FILE)
                    .output(**outputs)
                    .global_args('-progress', 'pipe:1', '-loglevel', 'error', *global_args)
                    .overwrite_output()
                    .run_async(pipe_stdout=True, pipe_stderr=True, cmd=self.ffmpeg_location)
                ), total_duration, errors=True)
        except ffmpeg.Error:
            sys.stdout.write('FFmpeg error, perhaps the file cannot be found or the input is not valid\n')
            pass
            sys.exit(1)
        except Exception as e:
            sys.stdout.write(e)
            pass
            sys.exit(1)
        finally:
            sys.stdout.write(result)
            sys.exit(0)    


if __name__ == '__main__':
    available_effects = ['hflip', 'vflip', 'q', 't', 'a', 'f', 's', 'd', 'tb']

    # Required Arguments
    parser = argparse.ArgumentParser(description='Processing effects for video')
    parser.add_argument('IN_FILE', type=str, help='Input filename')
    parser.add_argument('OUT_FILE', type=str, help='Output filename')
    parser.add_argument('EFFECT', choices=available_effects, help='''Video processing effects [hflip, vflip, q, t, a, f, s, d, tb];
                        Video Flip [hflip, vflip];
                        Video Lower Quality [q];
                        Audio/Video Trim (requires additional params) [t];
                        Audio/Video Concatenation (requires additional params) [a];
                        Audio/Video Change Speed (requires additional params) [f];
                        Video Hue Saturation (requires additional params) [s];
                        Draw Text (requires additional params) [d];
                        Create Video Thumbail (requires additional params) [tb]''')

    # Optional Arguments
    parser.add_argument('-l', '--ffmpeg_location', type=str, default='ffmpeg.exe', help='FFmpeg location')
    parser.add_argument('-t', '--trim', type=str, help='Range to trim (start time : end time, ex. 0:90)')
    parser.add_argument('-a', '--add_file', type=str, help='Two files to concatenate (additional filename)')
    parser.add_argument('-f', '--factor', type=float, help='Factor to speed up audio or video')
    parser.add_argument('-s', '--saturation', type=int, help='Hue Saturation Value (integer between -10 and 10)')
    parser.add_argument('-d', '--draw_text', type=str, help='Text to be drawn')
    parser.add_argument('-x', '--x_coord', type=float, default=0.0, help='Text Position (x-coordinate)')
    parser.add_argument('-y', '--y_coord', type=float, default=0.0, help='Text Position (y-coordinate)')
    parser.add_argument('-tb', '--thumbnail', type=float, default=0.0, help='Time offset (10 seconds, ex. 10)')

    args = parser.parse_args()
    
    if not args.IN_FILE or not args.OUT_FILE:
        sys.stdout.write('No file provided through IN_FILE or OUT_FILE')
        sys.stdout.write('\nType -h or --help for usage\n')
    elif not args.EFFECT:
        sys.stdout.write('No effect provided through EFFECT')
        sys.stdout.write('\nType -h or --help for usage\n')
    elif not is_file(args.IN_FILE) and not is_file(args.OUT_FILE):
        sys.stdout.write('Incorrect file input through IN_FILE or OUT_FILE')
        sys.stdout.write('\nType -h or --help for usage\n')
    else:
        additional_args = AdditionalArgs(args.trim, args.add_file, args.factor, args.saturation,
                    args.draw_text, args.x_coord, args.y_coord, args.thumbnail)
        VideoEffect(args.IN_FILE, args.OUT_FILE, args.EFFECT, args.ffmpeg_location, additional_args).video_effect()