#!/usr/bin/python

from PIL import Image
from datetime import datetime
import hashlib
import time
import os
import random
import shutil
import sys

PIC_EXTS = { "JPG", "PNG", "JPEG" }
PIC_DEST = 'Photos'
MOV_EXTS = { 'MOV', 'M4V', 'MP4' }
MOV_DEST = 'Movies'

def log(message):
    print '%s' % message

"""
Calculate the md5 of the file.
"""
def md5(fname):
    MAX_READ = 400 * 1024
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        # a wild guess
        chunk = f.read(MAX_READ)
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

"""
Returns True when the given two files are identical.
"""
def is_file_same(src, dest):
    # todo: can be optimized
    return md5(src) == md5(dest)
    
"""
Move the item to the ROOT directory with the date.
"""
class MoveCode(object):
    SUCCESS = 0
    DUPLICATE = 1
    SAME_NAME = 2
    FAILED = 3
    @staticmethod
    def get_size():
        return 4
    
def move_file(file_name, file_path, date, root):
    if not isinstance(date, datetime):
        raise RuntimeError('Given date is not a valid datetime type value.')

    month = '%02d' % date.month
    year = '%02d' % date.year
    day = '%02d' % date.day
    dest_path = os.path.join(root, year, month, day)

    # creates new folder
    if not os.path.exists(dest_path):
        log('Create folder %s' % dest_path)
        os.makedirs(dest_path)
        
    # check whether file exists
    new_file_path = os.path.join(dest_path, file_name)
    return_code = MoveCode.SUCCESS
    if os.path.isfile(new_file_path):
        if is_file_same(file_path, new_file_path):
            log('File %s already exists in %s, ignore' % (file_path, new_file_path))
            return MoveCode.DUPLICATE
        else:
            # generate a new file name with random suffix
            suffix = random.randint(0, 1 << 16)
            dest_path = os.path.join(dest_path, '%s_%d' % (file_name, suffix))
            return_code = MoveCode.SAME_NAME
    try:        
        shutil.move(file_path, dest_path)
    except Exception as ex:
        log('File %s is failed to move', file_path)
        return_code = MoveCode.FAILED
    return return_code

"""
Return True when the filename is a picture.
"""
def is_a_pic(name):
    if len(name.split('.')) < 2:
        return False
    ext = name.split('.')[-1]
    return ext.upper() in PIC_EXTS

"""
Return True when the filename is a movie.
"""
def is_a_movie(name):
    if len(name.split('.')) < 2:
        return False
    ext = name.split('.')[-1]
    return ext.upper() in MOV_EXTS

""" 
Return True when the item is a valid photo or movie.
"""
def is_valid_item(name):
    # hidden file
    if name.startswith("._"):
        return False
    if is_a_pic(name) or is_a_movie(name):
        return True
    return False

"""
Returns the date when the given picture is captured. Returns None when the capture date
does not exist in the original file.
"""
def get_image_date(filepath):
    KEY = 36867
    result = None
    try:
        with Image.open(file_path) as img:
            exif = img._getexif()
            # check the existence of the date 
            if exif.has_key(KEY) and exif[KEY] is not None:
                # convert to datetime
                value = exif[KEY][0]
                result = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as ex:
        log("Open Image {0} failed {1}".format(file_path, ex.message))
    return result

"""
Returns the date when the given movie is captured. Returns None when the capture date
does not exist in the original file.
"""
def get_movie_date(filepath):
    return None

"""
Returns the date of the file creation. 
"""
def get_file_date(filepath):
    time_value = time.ctime(os.path.getmtime(filepath))
    return datetime.strptime(time_value, "%a %b %d %H:%M:%S %Y")

# Main entry
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "%s <dirname> <image root>" % sys.argv[0]
        sys.exit(1)

    (script, dirname, root_dest) = sys.argv
    non_imgs = []
    broken_imgs = []
    empty_date_imgs = []
    empty_date_movs = []
    img_count = 0
    mov_count = 0
    move_count = [0] * MoveCode.get_size()
    
    for root, dirs, files in os.walk(dirname):
        for name in files:
            file_path = os.path.join(root, name)
            # check file validation
            if not is_valid_item(file_path):
                non_imgs.append(file_path)
                continue

            dest_path = root_dest
            date = None
            if is_a_pic(name):
                img_count = img_count + 1
                date = get_image_date(file_path)
                dest_path = os.path.join(root_dest, PIC_DEST)
                if date is None:
                    empty_date_imgs.append(file_path)
            elif is_a_movie(name):
                mov_count = mov_count + 1
                date = get_movie_date(file_path)
                dest_path = os.path.join(root_dest, MOV_DEST)
                if date is None:
                    empty_date_movs.append(file_path)
                
            # if there is no date information, we will use the file date
            if date is None:
                date = get_file_date(file_path)
                # for now, does not know how to get the movie date
                if is_a_pic(name):
                    log('Cannot parse the date of %s, use file creation time %s' % (file_path, date))

            # move the file
            rc = move_file(name, file_path, date, dest_path)
            move_count[rc] = move_count[rc] + 1
    log('-------------------------')
    log('Total Images:      %25d' % img_count)
    log('Non Images:        %25d' % len(non_imgs))
    log('Empty Date Images: %25d' % len(empty_date_imgs))
    log('Empty Date Movies: %25d' % len(empty_date_movs))
    log('Move             : %25d' % move_count[MoveCode.SUCCESS])
    log('Duplicate        : %25d' % move_count[MoveCode.DUPLICATE])
    log('Same File Name   : %25d' % move_count[MoveCode.SAME_NAME])
    log('Failure Count    : %25d' % move_count[MoveCode.FAILED])
