from __future__ import unicode_literals, print_function
import argparse
import sys
import warnings
warnings.filterwarnings('ignore')

from PIL import Image
from utils.checkfile import check_file


parser = argparse.ArgumentParser(description='Convert image files')
parser.add_argument('-i', '--in_file', help='Input filename')
parser.add_argument('-o', '--out_file', help='Output filename')
parser.add_argument('-f', '--format', help='''Input Image Formats [png, jpg, jpeg, ico, webp, bmp],
                    Output Image Formats [png, jpg, ico, webp, bmp, pdf]''')
parser.add_argument('-s', '--icon_size', type=int, default=32, help='''Icon Image Sizes [16, 24, 32, 48, 64, 128, 256]''')


def image_convert(in_file, out_file, format, icon_size):
        output_file = out_file.split('.')[0]
        # Check if input file is a file
        if check_file(in_file):
            # Checks if format is *.ico but input size is not valid
            if in_file.lower().endswith(('.ico')) and icon_size not in [16, 24, 32, 48, 64, 128, 256]:
                sys.stdout.write('Icon size not valid.\n')
                sys.exit(0)
            # Checks if the extension of the input file is valid
            if in_file.lower().endswith(('.png', 'jpg', '.jpeg', '.ico', '.webp', '.bmp')):
                img = Image.open(in_file).convert('RGB')
                # File output based on input format
                if format.lower() in ['png', 'pdf', 'bmp']:
                    img.save(f'{output_file}.{format}', format)
                elif format.lower() == 'jpg':
                    img.save(f'{output_file}.jpg', 'jpeg')
                elif format.lower() == 'ico':
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
                elif format.lower() == 'webp':
                    img.save(f'{output_file}.webp', 'webp', lossless=True, quality=100, method=6)
                else:
                    sys.stdout.write('Invalid output file format.\n')
                    sys.exit(0)
            else:
                sys.stdout.write('Input file extension not accepted.\n')
                sys.exit(0)
        else:
            sys.stdout.write('Invalid input file format.\n')
            sys.exit(0)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.in_file or not args.out_file:
        sys.stdout.write('No file provided through --in_file or --out_file')
        sys.stdout.write('\nType -h or --help for usage\n')
        sys.exit(0)
    if not args.format:
        sys.stdout.write('Format not provided through -f or --format')
        sys.stdout.write('\nType -h or --help for usage\n')
        sys.exit(0)
    else:
        image_convert(args.in_file, args.out_file, args.format, args.icon_size)