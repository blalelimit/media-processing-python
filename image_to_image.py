from __future__ import unicode_literals, print_function
import argparse
import sys
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
from PIL import Image
from uuid import uuid4
from pdf2image import convert_from_path, exceptions
from utils.scanfile import is_file


def set_range(value):
    value_ = int(value)
    if value_ < 50 or value_ > 800:
        raise argparse.ArgumentTypeError('%s is an invalid value, choose from range [50-800]' % value)
    return value_


def set_arguments():
    # Available Inputs
    available_formats = ['png', 'jpg', 'jpeg', 'ico', 'webp', 'bmp', 'pdf']
    available_sizes = [16, 24, 32, 48, 64, 128, 256]

    # Required Arguments
    parser = argparse.ArgumentParser(description='Convert image file formats', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('IN_FILE', type=str, help='Input filename')
    parser.add_argument('OUT_FILE', type=str, help='Output filename')
    parser.add_argument('FORMAT', choices=available_formats, type=str,
            help='''Image Formats [png, jpg, jpeg, ico, webp, bmp, pdf]''')

    # Optional Arguments
    parser.add_argument('-s', '--icon_size', choices=available_sizes,
            type=int, default=32, help='''Icon Image Sizes [16, 24, 32, 48, 64, 128, 256]''')
    parser.add_argument('-d', '--dpi', type=set_range, default=200, help='DPI (for pdf to image)')
    parser.add_argument('-l', '--poppler_location', type=str, default='bin/', help='Poppler location (for pdf to image)')

    
    # Set Argument Parser
    args = parser.parse_args()

    return args


class ImageToImage:
    def __init__(self, in_file, out_file, out_format, icon_size, dpi, poppler_location):
        self.in_file = in_file
        self.out_file = out_file
        self.out_format = out_format
        self._out_name = None
        self._in_format = None
        self.icon_size = icon_size
        self.dpi = dpi
        self.poppler_location = poppler_location


    @property
    def out_name(self):
        return '.'.join(self.in_file.split('.')[:-1])
    

    @property
    def in_format(self):
        return self.in_file.split('.')[-1].lower()


    def pdf_to_image(self):
        try:
            pages = convert_from_path(pdf_path=self.in_file, dpi=self.dpi, transparent=False,
                size=None, poppler_path=self.poppler_location)[0]
            
            if self.out_format in ['jpg', 'jpeg']:
                pages.save(f'{self.out_file}.{self.out_format}', 'JPEG')

            elif self.out_format in ['png', 'ico', 'webp', 'bmp']:
                temp = uuid4()
                pages.save(f'{temp}.jpg', 'JPEG')
                img = Image.open(f'{temp}.jpg').convert('RGB')
                if self.out_format == 'ico':
                    self.image_to_ico(img)
                else:
                    img.save(f'{self.out_file}.{self.out_format}', self.out_format)
                Path(f'{temp}.jpg').unlink()
        except exceptions.PDFInfoNotInstalledError:
            sys.stdout.write('Poppler cannot be found, specify Poppler path with -l or --poppler_location\n')
            sys.exit(0)


    
    def image_to_ico(self, img):
        x, y = img.size
        z = abs(int((x - y) / 2))
        # set dimensions equal by resizing
        if x < y:
            img = img.resize(size=(x, x), resample=4, box=(0, z, x, x + z), reducing_gap=None)
        elif x > y:
            img = img.resize(size=(y, y), resample=4, box=(z, 0, y + z, y), reducing_gap=None)
        # resize if too small
        if min(img.size) < self.icon_size:
            img = img.resize(size=(self.icon_size, self.icon_size), resample=2, box=None, reducing_gap=None)
        img.save(f'{self.out_file}.ico', sizes=[(self.icon_size, self.icon_size)])


    def image_convert(self):
        # FileNotFound
        if not is_file(self.in_file):
            sys.stdout.write('Input file cannot be found.\n')
            sys.exit(0)
        
        # Format is *.ico but input size is not valid
        if self.in_format == 'ico' and self.icon_size not in [16, 24, 32, 48, 64, 128, 256]:
            sys.stdout.write('Icon size not valid.\n')
            sys.exit(0)

        # Main Image to Image Convertor
        if self.in_format == 'pdf':
            self.pdf_to_image()

        elif self.in_format in ['png', 'jpg', 'jpeg', 'ico', 'webp', 'bmp']:
            img = Image.open(self.in_file).convert('RGB')
            # File output based on input format
            if self.out_format == 'bmp':
                img.save(f'{self.out_file}.bmp', 'bmp')

            elif self.out_format == 'png':
                img.save(f'{self.out_file}.png', 'png', compress_level=0)

            elif self.out_format in ['jpg', 'jpeg']:
                img.save(f'{self.out_file}.{self.out_format}', 'jpeg')

            elif self.out_format == 'ico':
                self.image_to_ico(img)

            elif self.out_format == 'webp':
                img.save(f'{self.out_file}.webp', 'webp', lossless=True, quality=100, method=6)

            elif self.out_format == 'pdf':
                 img.save(f'{self.out_file}.pdf', 'pdf', resolution=100)

            else:
                sys.stdout.write('Invalid output file format.\n')
                sys.exit(0)
            
        else:
            sys.stdout.write('Input file extension not accepted.\n')
            sys.exit(0)


if __name__ == '__main__':
    args = set_arguments()

    if args.IN_FILE.split('.')[-1] == args.FORMAT:
        sys.stdout.write('Invalid input, same file formats in IN_FILE and FORMAT\n')
        sys.exit(0)
    else:
        img_to_img = ImageToImage(args.IN_FILE, args.OUT_FILE, args.FORMAT, args.icon_size, args.dpi, args.poppler_location)
        img_to_img.image_convert()
        sys.stdout.write('Image file format conversion successful\n')


    

    