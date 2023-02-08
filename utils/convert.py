import ffmpeg
from PIL import Image
from os import path


pathFile = 'static/inputs'
pathFileSave = 'static/outputs'


class MediaConvert:
    def __init__(self, uuid_filename, filename, file_format):
        self.uuid_filename = uuid_filename
        self.filename = filename
        self.file_format = file_format

    def image_convert(self, icon):
        img = Image.open(path.join(pathFile, f'{self.uuid_filename}.{self.filename[1]}'))

        if self.file_format == 'png':
            img.save(path.join(pathFileSave, f'{self.filename[0]}.png'), 'png')

        elif self.file_format == 'jpg' or self.file_format == 'jpeg':
            img.save(path.join(pathFileSave, f'{self.filename[0]}.{self.file_format}'), 'jpeg')

        elif self.file_format == 'ico':
            icon = int(icon)
            x, y = img.size
            z = abs(int((x - y) / 2))
            # set dimensions equal by resizing
            if x < y:
                img = img.resize(size=(x, x), resample=4, box=(0, z, x, x + z), reducing_gap=None)
            elif x > y:
                img = img.resize(size=(y, y), resample=4, box=(z, 0, y + z, y), reducing_gap=None)
            # resize if too small
            if min(img.size) < icon:
                img = img.resize(size=(icon, icon), resample=2, box=None, reducing_gap=None)
            img.save(path.join(pathFileSave, f'{self.filename[0]}.ico'), sizes=[(icon, icon)])
            # default sizes -> sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

        elif self.file_format == 'webp':
            img.save(path.join(pathFileSave, f'{self.filename[0]}.webp'), 'webp',
                     lossless=True, quality=100, method=6)

        elif self.file_format == 'pdf':
            img.save(path.join(pathFileSave, f'{self.filename[0]}.pdf'), 'pdf')

        elif self.file_format == 'bmp':
            img.save(path.join(pathFileSave, f'{self.filename[0]}.bmp'), 'bmp')

        else:
            img.save(path.join(pathFileSave, f'{self.filename[0]}.png'), 'png')

    def audio_convert(self):
        in_file = ffmpeg.input(path.join(pathFile, f'{self.uuid_filename}.{self.filename[1]}'))
        try:
            if self.file_format in ['mp3', 'opus', 'flac', 'wav']:
                (
                    ffmpeg
                    .output(in_file, path.join(pathFileSave, f'{self.filename[0]}.{self.file_format}'))
                    .run(overwrite_output=True, cmd='ffmpeg.exe', capture_stdout=True, capture_stderr=True)
                )

            else:
                (
                    ffmpeg
                    .output(in_file, path.join(pathFileSave, f'{self.filename[0]}.mp3'))
                    .run(overwrite_output=True, cmd='ffmpeg.exe', capture_stdout=True, capture_stderr=True)
                )
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))

    def video_convert(self, gif):
        in_file = ffmpeg.input(path.join(pathFile, f'{self.uuid_filename}.{self.filename[1]}'))
        try:
            if self.file_format == 'gif':
                fps, scale = gif.split(', ')
                (
                    ffmpeg
                    .output(in_file, path.join(pathFileSave, f'{self.filename[0]}.gif'),
                            ss=0, t=3, vf=f'fps={fps},scale={scale}:-1:flags=lanczos', loop=0)
                    .run(overwrite_output=True, cmd='ffmpeg.exe', capture_stdout=True, capture_stderr=True)
                )

            elif self.file_format in ['mp4', 'mkv', 'avi', 'mov']:
                (
                    ffmpeg
                    .output(in_file, path.join(pathFileSave, f'{self.filename[0]}.{self.file_format}'),
                            vcodec='copy')
                    .run(overwrite_output=True, cmd='ffmpeg.exe', capture_stdout=True, capture_stderr=True)
                )

            else:
                (
                    ffmpeg
                    .output(in_file, path.join(pathFileSave, f'{self.filename[0]}.mp4'),
                            vcodec='copy')
                    .run(overwrite_output=True, cmd='ffmpeg.exe', capture_stdout=True, capture_stderr=True)
                )
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
