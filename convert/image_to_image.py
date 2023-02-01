from __future__ import unicode_literals, print_function
import argparse
from PIL import Image


parser = argparse.ArgumentParser(description='Convert image files')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-f', '--format', help='''Input Image Formats [png, jpg, jpeg, ico, webp, bmp],
                    Output Image Formats [png, jpg, ico, webp, bmp, pdf]''')
parser.add_argument('-s', '--icon_size', type=int, default=32, help='''Icon Image Sizes [16, 24, 32, 48, 64, 128, 256]''')


def image_convert(in_file, out_file, format, icon_size):
        input_file = in_file.split('.')
        output_file = out_file.split('.')[0]
        old_format = input_file[len(input_file)-1]

        if old_format not in ['png', 'jpg', 'jpeg', 'ico', 'webp', 'bmp']:
            print('Invalid file format')
        else:
            img = Image.open(in_file).convert('RGB')
            
            if format in ['png', 'pdf', 'bmp']:
                img.save(f'{output_file}.{format}', format)
            elif format == 'jpg':
                img.save(f'{output_file}.jpg', 'jpeg')
            elif format == 'ico':
                x, y = img.size
                z = abs(int((x - y) / 2))
                # set dimensions equal by resizing
                if x < y:
                    img = img.resize(size=(x, x), resample=4, box=(0, z, x, x + z), reducing_gap=None)
                elif x > y:
                    img = img.resize(size=(y, y), resample=4, box=(z, 0, y + z, y), reducing_gap=None)
                # resize if too small
                if min(img.size) < icon_size:
                    img = img.resize(size=(icon_size, icon_size), resample=2, box=None, reducing_gap=None)
                img.save(f'{output_file}.ico', sizes=[(icon_size, icon_size)])
            elif format == 'webp':
                img.save(f'{output_file}.webp', 'webp', lossless=True, quality=100, method=6)
            else:
                print('Invalid file type')


if __name__ == '__main__':
    args = parser.parse_args()
    image_convert(args.in_file, args.out_file, args.format, args.icon_size)