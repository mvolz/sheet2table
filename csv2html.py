#Licensed as x11 from mvolz.com
#This basically means do what you want with it.
#sorttable.js from http://www.kryogenix.org/code/browser/sorttable/
#and is also under an x11 license

#How to use: run 'python csv2html.py inputfile.csv output.html'
#contents of output.html contains .js, .css, and .html and can be pasted
#into wordpress posts or what have you.

import csv

def csv2html(input,output):

	htmlfile = open(output,"w")	
	
	#r+w css file
	css = open("tablestyle.css","r") 
	htmlfile.write("<style>\n<!--"+css.read()+"-->\n</style>\n")
	css.close()
	
	#r+w .js file
	htmlfile.write("<script language='javascript' type='text/javascript' >\n")
	js = open("sorttable.js","r")
	htmlfile.write(js.read())
	htmlfile.write("</script>\n")
	js.close()
	
	#read csv
	csvfile = open(input,"r")
	#checks format of csv for interpretation
	dialect = csv.Sniffer().sniff(csvfile.read(1024)) #1024 is the amt. of file to sample to determine format
	#reset file position
	csvfile.seek(0)
	reader = csv.reader(csvfile, dialect)
	
	#write html
	htmlfile.write("<table class='sortable'>\n")
	i=0
	for row in reader:
		if i==0:
			#header
			htmlfile.write("\t<tr>\n")
			for column in row:
				htmlfile.write("\t\t<th>"+column+"</th>\n")
		elif i % 2 == 0:
			htmlfile.write("\t<tr id ='even'>\n")
			for column in row:
				htmlfile.write("\t\t<td>"+column+"</td>\n")
		else:
			htmlfile.write("\t<tr id ='odd'>\n")
			for column in row:
				htmlfile.write("\t\t<td>"+column+"</td>\n")
					
		i+=1
		htmlfile.write("\t</tr>\n")
	htmlfile.write("</table>\n")
	
	csvfile.close()
	htmlfile.close()
	print "%s successfully created." % output


if __name__ == "__main__":
	from sys import argv
	from os.path import isfile
	
	if len(argv) == 3:
		input = argv[1]
		output = argv[2]
	else:
		print "Please supply two arguments, like so:\npython csv2html.py input.csv output.html"
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
	
	csv2html(input,output)
