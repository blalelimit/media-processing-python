from __future__ import unicode_literals, print_function
import argparse
import sys
import warnings
warnings.filterwarnings('ignore')

from PIL import Image
from utils.scanfile import is_file


def image_convert(IN_FILE, OUT_FILE, FORMAT, icon_size):
        output_file = OUT_FILE.split('.')[0]
        format = FORMAT
        # Check if input file is a file
        if is_file(IN_FILE):
            # Checks if format is *.ico but input size is not valid
            if IN_FILE.lower().endswith(('.ico')) and icon_size not in [16, 24, 32, 48, 64, 128, 256]:
                sys.stdout.write('Icon size not valid.\n')
                sys.exit(0)
            # Checks if the extension of the input file is valid
            if IN_FILE.lower().endswith(('.png', 'jpg', '.jpeg', '.ico', '.webp', '.bmp')):
                img = Image.open(IN_FILE).convert('RGB')
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
    available_formats = ['png', 'jpg', 'ico', 'webp', 'bmp', 'pdf']
    available_sizes = [16, 24, 32, 48, 64, 128, 256]

    # Required Arguments
    parser = argparse.ArgumentParser(description='Convert image files')
    parser.add_argument('IN_FILE', type=str, help='Input filename')
    parser.add_argument('OUT_FILE', type=str, help='Output filename')
    parser.add_argument('FORMAT', choices=available_formats, type=str, help='''Input Image Formats [png, jpg, jpeg, ico, webp, bmp],
                    Output Image Formats [png, jpg, ico, webp, bmp, pdf]''')

    # Optional Arguments
    parser.add_argument('-s', '--icon_size', choices=available_sizes,
                    type=int, default=32, help='''Icon Image Sizes [16, 24, 32, 48, 64, 128, 256]''')

    args = parser.parse_args()

    if not args.IN_FILE or not args.OUT_FILE:
        sys.stdout.write('No file provided through IN_FILE or OUT_FILE')
        sys.stdout.write('\nType -h or --help for usage\n')
        sys.exit(0)
    if not args.FORMAT:
        sys.stdout.write('Format not provided through FORMAT')
        sys.stdout.write('\nType -h or --help for usage\n')
        sys.exit(0)
    else:
        image_convert(args.IN_FILE, args.OUT_FILE, args.FORMAT, args.icon_size)