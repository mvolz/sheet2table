#!/usr/bin/python
#
# Convert spreadsheet to CSV file. From Mitch Frazier.
# http://www.linuxjournal.com/content/convert-spreadsheets-csv-files-python-and-pyuno
#
# Based on:
#   PyODConverter (Python OpenDocument Converter) v1.0.0 - 2008-05-05
#   Copyright (C) 2008 Mirko Nasato <mirko@artofsolving.com>
#   Licensed under the GNU LGPL v2.1 - or any later version.
#   http://www.gnu.org/licenses/lgpl-2.1.html
#
import uno
from com.sun.star.task import ErrorCodeIOException

import os
import ooutils


class SSConverter:
    """
    Spreadsheet converter class.
    Converts spreadsheets to CSV files.
    """

    def __init__(self, oorunner=None):
        self.desktop  = None
        self.oorunner = None


    def convert(self, inputFile, outputFile):
        """
        Convert the input file (a spreadsheet) to a CSV file.
        """

        # Start openoffice if needed.
        if not self.desktop:
            if not self.oorunner:
                self.oorunner = ooutils.OORunner()

            self.desktop = self.oorunner.connect()

        inputUrl  = uno.systemPathToFileUrl(os.path.abspath(inputFile))
        outputUrl = uno.systemPathToFileUrl(os.path.abspath(outputFile))
        document  = self.desktop.loadComponentFromURL(inputUrl, "_blank", 0, ooutils.oo_properties(Hidden=True))

        try:
            # Additional property option:
            #   FilterOptions="59,34,0,1"
            #     59 - Field separator (semicolon), this is the ascii value.
            #     34 - Text delimiter (double quote), this is the ascii value.
            #      0 - Character set (system).
            #      1 - First line number to export.
            #
            # For more information see:
            #   http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options
            #
            document.storeToURL(outputUrl, ooutils.oo_properties(FilterName="Text - txt - csv (StarCalc)"))
        finally:
            document.close(True)


if __name__ == "__main__":
    from sys import argv
    from os.path import isfile

    if len(argv) == 2  and  argv[1] == '--shutdown':
        ooutils.oo_shutdown_if_running()
    else:
        if len(argv) < 3  or  len(argv) % 2 != 1:
            print "USAGE:"
            print "  python %s INPUT-FILE OUTPUT-FILE INPUT-FILE OUTPUT-FILE..." % argv[0]
            print "OR"
            print "  python %s --shutdown" % argv[0]
            exit(255)
        if not isfile(argv[1]):
            print "File not found: %s" % argv[1]
            exit(1)

        try:
            i = 1
            converter = SSConverter()

            while i+1 < len(argv):
                print '%s => %s' % (argv[i], argv[i+1])
                converter.convert(argv[i], argv[i+1])
                i += 2

        except ErrorCodeIOException, exception:
            print "ERROR! ErrorCodeIOException %d" % exception.ErrCode
            exit(1)

