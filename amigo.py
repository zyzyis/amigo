#!/usr/bin/python
__author__ = "Si Yin"
__email__ = "zyzyis@gmail.com"
__license__ = "MIT"

import hashlib
import time
import os
import random
import shutil
import sys
from datetime import datetime
from PIL import Image

class Logger(object):
    """
    A simple logger.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def prt(self, message, color=''):
        """ print """
        print '%s%s%s' % (color, message, self.ENDC)

    def info(self, message):
        """ info print """
        print "%s[info]%s %s" % (self.HEADER, self.ENDC, message)

    def fail(self, message):
        """ failure print """
        print "%s[fail]%s %s" % (self.FAIL, self.ENDC, message)

logger = Logger()

class FileUtil(object):
    """
    File utilities.
    """
    def _md5sum(self, fname):
        """
        Calculate the md5 of the file.
        """
        CHUNK_SIZE = 400 * 1024
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            # a wild guess
            chunk = f.read(CHUNK_SIZE)
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def is_file_same(self, src, dest):
        """
        Returns True when the given two files are identical.
        """
        return self._md5sum(src) == self._md5sum(dest)

    def move_file(self, file_name, file_path, date, root):
        """
        Move file from one path to the other with the given date information.
        Args:
        file_name: original file name.
        file_path: original full file path (include file name).
        date: date value.
        root: the destination path where the file is moved to.

        Returns:
        A move code.
        """
        if not isinstance(date, datetime):
            raise RuntimeError('Given date is not a valid datetime type value.')

        month = '%02d' % date.month
        year = '%02d' % date.year
        day = '%02d' % date.day
        dest_path = os.path.join(root, year, month, day)

        # creates new folder
        if not os.path.exists(dest_path):
            logger.info('Create folder %s' % dest_path)
            os.makedirs(dest_path)

        # check whether file exists
        new_file_path = os.path.join(dest_path, file_name)
        return_code = MoveCode.SUCCESS
        if os.path.isfile(new_file_path):
            if self.is_file_same(file_path, new_file_path):
                logger.info('File %s already exists in %s, ignore' % (file_path, new_file_path))
                return MoveCode.DUPLICATE
            else:
                # generate a new file name with random suffix
                suffix = random.randint(0, 1 << 16)
                dest_path = os.path.join(dest_path, '%s_%d' % (file_name, suffix))
                return_code = MoveCode.SAME_NAME
        try:
            shutil.move(file_path, dest_path)
        except Exception as ex:
            logger.fail('File %s is failed to move' % file_path)
            return_code = MoveCode.FAILED
        return return_code

    def get_file_date(self, filepath):
        """
        Returns the date of the file creation.
        """
        time_value = time.ctime(os.path.getmtime(filepath))
        return datetime.strptime(time_value, "%a %b %d %H:%M:%S %Y")
class MoveCode(object):
    """
    Move the item to the ROOT directory with the date.
    """
    SUCCESS = 0
    DUPLICATE = 1
    SAME_NAME = 2
    FAILED = 3
    @staticmethod
    def get_size():
        return 4

class Amigo(object):
    """
    The Main class contains the business logic.
    """
    def __init__(self, pic_root='Photos', mov_root='Movies'):
        self.pic_root = pic_root
        self.mov_root = mov_root
        self.pic_exts = {"JPG", "PNG", "JPEG"}
        self.mov_exts = {'MOV', 'M4V', 'MP4', 'AVI'}

        # files which are not images nor movies.
        self.non_imgs = []
        # files which cannot be moved.
        self.broken_imgs = []
        # images which do not contain date information
        self.empty_date_imgs = []
        # movies which do not contain date information
        self.empty_date_movs = []
        # total images count
        self.img_count = 0
        # total movie count
        self.mov_count = 0
        # move statistics
        self.move_count = [0] * MoveCode.get_size()

    def is_a_pic(self, name):
        """
        Return True when the filename is a picture.
        """
        if len(name.split('.')) < 2:
            return False
        ext = name.split('.')[-1]
        return ext.upper() in self.pic_exts

    def is_a_movie(self, name):
        """
        Return True when the filename is a movie.
        """
        if len(name.split('.')) < 2:
            return False
        ext = name.split('.')[-1]
        return ext.upper() in self.mov_exts

    def is_valid_item(self, name):
        """
        Return True when the item is a valid photo or movie.
        """
        # hidden file
        if name.startswith("._"):
            return False
        if self.is_a_pic(name) or self.is_a_movie(name):
            return True
        return False

    def get_image_date(self, file_path):
        """
        Returns the date when the given picture is captured. Returns None when the capture date
        does not exist in the original file.
        """
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
            logger.fail("Open Image {0} failed {1}".format(file_path, ex.message))
        return result

    def get_movie_date(self, filepath):
        """
        Returns the date when the given movie is captured. Returns None when the capture date
        does not exist in the original file.
        """
        return None

    def run(self, src, dst):
        """
        Run the movement from source directory to the destination directory.
        """
        for root, dirs, files in os.walk(src):
            for name in files:
                file_path = os.path.join(root, name)
                # check file validation
                if not self.is_valid_item(file_path):
                    self.non_imgs.append(file_path)
                    continue

                dest_path = dst
                date = None
                if self.is_a_pic(name):
                    self.img_count = self.img_count + 1
                    date = self.get_image_date(file_path)
                    dest_path = os.path.join(dst, self.pic_root)
                    if date is None:
                        self.empty_date_imgs.append(file_path)
                elif self.is_a_movie(name):
                    self.mov_count = self.mov_count + 1
                    date = self.get_movie_date(file_path)
                    dest_path = os.path.join(dst, self.mov_root)
                    if date is None:
                        self.empty_date_movs.append(file_path)

                file_util = FileUtil()
                # if there is no date information, we will use the file date
                if date is None:
                    date = file_util.get_file_date(file_path)
                    # for now, does not know how to get the movie date
                    if self.is_a_pic(name):
                        logger.info('Cannot parse the date of %s, use file creation time %s' \
                            % (file_path, date))

                # move the file
                rc = file_util.move_file(name, file_path, date, dest_path)
                self.move_count[rc] = self.move_count[rc] + 1

    def print_result(self):
        logger.prt('-------------------------')
        logger.prt('Total Images     : %25d' % self.img_count)
        logger.prt('Empty Date Images: %25d' % len(self.empty_date_imgs))
        logger.prt('Non Images       : %25d' % len(self.non_imgs))
        logger.prt('Empty Date Movies: %25d' % len(self.empty_date_movs))
        logger.prt('Move             : %25d' % self.move_count[MoveCode.SUCCESS])
        logger.prt('Duplicate        : %25d' % self.move_count[MoveCode.DUPLICATE])
        logger.prt('Same File Name   : %25d' % self.move_count[MoveCode.SAME_NAME])
        logger.prt('Failure Count    : %25d' % self.move_count[MoveCode.FAILED])

# Main
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "%s <dirname> <image root>" % sys.argv[0]
        sys.exit(1)

    (script, src, dst) = sys.argv
    amigo = Amigo()
    amigo.run(src, dst)
    amigo.print_result()
