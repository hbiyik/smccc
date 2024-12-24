"""
 Copyright (C) 2024 boogie

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import copy


MAPPING = {'DEBUG': 37,  # white
           'INFO': 36,  # cyan
           'AGR': 32,  # green
           'WARNING': 33,  # yellow
           'ERROR': 31,  # red
           'CRITICAL': 41,  # white on red bg
           }


class ColoredFormatter(logging.Formatter):

    def __init__(self, patern):
        logging.Formatter.__init__(self, patern)

    def format(self, record):
        colored_record = copy.copy(record)
        levelname = colored_record.levelname
        seq = MAPPING.get(levelname, 33)  # default white
        colored_levelname = ('{0}{1}m{2}{3}') \
            .format('\033[', seq, levelname, '\033[0m')
        colored_record.levelname = colored_levelname
        return logging.Formatter.format(self, colored_record)


logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = ColoredFormatter('%(levelname)18s | %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def setlevel(level):
    logger.setLevel(level)
    ch.setLevel(level)
