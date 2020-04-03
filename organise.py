from PIL import Image

import os
from datetime import datetime
import shutil
import argparse


parser = argparse.ArgumentParser(
    prog="Organise your pictures",
    usage="python organise.py (--move) -i [input folder] -o [output folder]",
    description=
    "This script will go over the photos in the input folder and "
    "for every month and year it will create sub folders in the main output folder "
    "where it will paste the pictures.\n"
    "It currently doesn't work with videos and it will skip the pictures that it can't find the date"
)

parser.add_argument(
    '-i', '--input-folder',
    type=str,
    required=True,
    help="The folder it will parse for pictures"
)
parser.add_argument(
    '-o', '--output-folder',
    type=str,
    required=True,
    help="The folder it will put the sub folders in"
)
parser.add_argument(
    '--move',
    action='store_true',
    help="Move and not just copy the pictures. By default it copies them"
)

args = parser.parse_args()

def get_date_taken(path):
    try:
        date_str = Image.open(path)._getexif()[36867][:10] # Ignore the time
    except KeyError:
        date_str = Image.open(path)._getexif()[306][:10] # Ignore the time
    return datetime.strptime(date_str, "%Y:%m:%d")

def foo(path):
    print(Image.open(path)._getexif())

if __name__ == "__main__":
    path = args.input_folder
    path_to_save = args.output_folder

    move = args.move

    for img in os.listdir(path):
        if img.split(".")[1] not in ['jpg', 'png', 'jpeg']:
            continue
        try:
            date = get_date_taken(f"{path}/{img}")
        except TypeError:
            continue

        if not os.path.isdir(f"{path_to_save}/{date.year}"):
            os.mkdir(f"{path_to_save}/{date.year}")
        if not os.path.isdir(f"{path_to_save}/{date.year}/{date.month:02}"):
            os.mkdir(f"{path_to_save}/{date.year}/{date.month:02}")

        if move:
            shutil.move(f"{path}/{img}", f"{path_to_save}/{date.year}/{date.month:02}")
        else:
            shutil.copy2(f"{path}/{img}", f"{path_to_save}/{date.year}/{date.month:02}")

    print("Done")
