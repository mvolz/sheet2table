#HOW TO USE

	#CONVERT FROM SPREADSHEET TO SORTABLE TABLE - LINUX/MACOS ONLY
	#run 'python spread2table.py input.odf output.html'
	#Current version only works on machines with openoffice installed on linux
	#for the spreadsheet -> .csv conversion. Also you'll probably have to 
	#play with the ooffice paths to get ssconverter.py working esp if on macos.
	#If you can't get it working export to .CSV and use csv2html.py.
	
	#CONVERT FROM .CSV TO SORTABLE TABLE - ALL OS - WINDOWS
	#run 'python csv2html.py input.csv output.html'
	#Input must be a .csv file. Most spreadsheet programs can export their
	#native filetype to .csv.

#LICENSING INFORMATION

#CSV2HTML.PY licensed as x11 from mvolz.com.
#SORTTABLE.JS from http://www.kryogenix.org/code/browser/sorttable/
#and is also under an x11 license
#OOUTILS.PY and SSCONVERTER.PY Copyright (C) 2008 Mirko Nasato 
#<mirko@artofsolving.com> and is modified by Mitch Frazier
#Licensed under the GNU LGPL v2.1 - or any later version.
#See files for more details

if __name__ == "__main__":
	
	from sys import argv
	import os
	from os.path import isfile
	from csv2html import csv2html
	import ssconverter 
	
	if len(argv) == 3:
		input = argv[1]
		output = argv[2]
	else:
		print "Please supply two arguments, like so:\npython sheet2table.py input.odf output.html"
		exit(255)
		
	if not isfile(input):
		print "%s not found. Please provide a valid file path." % input
		exit(1)
		
	if isfile (output):
		Yn = raw_input("%s already exists. This operation will overwrite that file. Do you want to continue? Y/n\n> " % output)
		if Yn == 'Y':
			print "Creating %s..." % output
		else:
			print "Canceling operation..."
			exit(1)
	
	converter = ssconverter.SSConverter()
	converter.convert(input, "HXz1SYGU.csv")
	csv2html("HXz1SYGU.csv", output)
	os.remove("HXz1SYGU.csv")
	
