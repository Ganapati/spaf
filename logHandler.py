#!/usr/bin/python

from mmap import mmap
import sys

class LogHandler:

    def __init__(self, filename):
        self.filename = filename
        self.last_line = self.get_last_lines(1)[0]

    def _reverse_file(self, f):
        """ Read file from end to start

        """
        mm = mmap(f.fileno(), 0)
        nl = mm.size() - 1
        prev_nl = mm.size()
        while nl > -1:
            nl = mm.rfind('\n', 0, nl)
            yield mm[nl + 1:prev_nl]
            prev_nl = nl + 1

    def get_last_lines(self, nb_lines):
        """ Read file line per line for nb_lines

        """
        lines = []
        with open(self.filename, 'r+') as infile:
            for line in self._reverse_file(infile):
                if nb_lines == 0:
                    break
                lines.append(line.rstrip())
                nb_lines = nb_lines - 1
        return lines[::-1]

    def get_lines_until(self, pattern):
        """ Read file line per line until pattern is matched

        """
        lines = []
        with open(self.filename, 'r+') as infile: 
            for line in self._reverse_file(infile):
                if pattern in line:
                    break
                lines.append(line.rstrip())
        return lines[::-1]

    def get_lines_until_last_check(self):
        """Read file from end until self.last_line reached

        """
        last_lines = self.get_lines_until(self.last_line)
        self.last_line = self.get_last_lines(1)[0]
        return last_lines
