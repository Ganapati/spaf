#!/usr/bin/python

import fnmatch
import os
import argparse
import glob
import re

class StaticPhpScanner:

    def __init__(self, folder=None, recursive=False):
        """Constructor

        """
        self.folder = folder
        self.recursive = recursive
        self.patterns = ['\$_(?P<method>(GET|POST|COOKIE))\[(\'|")(?P<var>[a-z0-9-_:]+)(\'|")\]',
                         '\$_(?P<method>SERVER)\[(\'|")(?P<var>(HTTP_REFERER|HTTP_USER_AGENT))(\'|")\]']

    def searchFiles(self, folder, recursive):
        """Search php files in folder

        """
        files = []
        if recursive:
            for root, dirnames, filenames in os.walk(folder):
                for filename in fnmatch.filter(filenames, '*.php'):
                    files.append(os.path.join(root, filename))
        else:
            files = glob.glob("%s/*.php" % folder)

        return files

    def parsePages(self, files):
        """Find entrypoint in files

        """
        result = {}
        compiledPatterns = []

        for pattern in self.patterns:
            regexp = re.compile(pattern, re.IGNORECASE)
            compiledPatterns.append(regexp)

        for file in files:
            result[file] = []
            with open(file, 'r') as lines:
                line_number = 0
                for line in lines:
                    line_number = line_number + 1
                    for pattern in compiledPatterns:
                        pattern_result = re.findall(pattern, line)
                        for m in pattern.finditer(line):
                            found = m.groupdict()
                            result[file].append({'line' : line_number,
                                                 'method' : found['method'],
                                                 'var' : found['var']})
            if len(result[file]) == 0:
                result.pop(file, None)
        return result

    def scan(self, output):
        """Begin file scanning

        """
        if output == "pretty":
            print "[*] Start static scan"
        files = self.searchFiles(self.folder, self.recursive)
        return self.parsePages(files)

if __name__ == "__main__":
    """Test method

    """
    parser = argparse.ArgumentParser(description='Scan static php files for injection points')
    parser.add_argument('-f', '--folder', action="store", dest="folder", required=True, help='Base folder')
    parser.add_argument('-r', '--recursive', action="store_true", dest="recursive", default=False, help='Recursive file search')
    args = parser.parse_args()

    sps = StaticPhpScanner(args.folder, args.recursive)
    result = sps.scan()
    for page, vars in result.items():
        print "[*] %s :" % page
        for var in vars:
            print " - line : %d > %s : %s" % (var['line'], var['method'], var['var'])
