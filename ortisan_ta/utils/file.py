# coding=utf-8
__author__ = 'Marcelo Ortiz'

import glob
import os
import pickle
from os.path import basename


def slice_files(pathname_pattern, max_lines, destination_dir, file_encoding: str = 'utf-8'):
    for file in glob.glob(pathname_pattern):
        smallfile = None
        with open(file, encoding=file_encoding) as bigfile:
            for lineno, line in enumerate(bigfile):
                if lineno % max_lines == 0:
                    if smallfile:
                        smallfile.close()
                    file_split = '{0}/{1}.{2:02d}'.format(destination_dir, basename(file), lineno)
                    smallfile = open(file_split, "w")
                if line.startswith('01'):
                    smallfile.write(line)
            if smallfile:
                smallfile.close()


def delete_files(cls, pathname_pattern):
    for file in glob.glob(pathname_pattern):
        os.remove(file)


def save_to_pickle(data, filename='file_example'):
    with open('%s.pickle' % (filename), 'wb') as handle:
        pickle.dump(data, handle)


def load_from_pickle(filename='file_example'):
    with open('%s.pickle' % (filename), 'rb') as handle:
        return pickle.load(handle)
