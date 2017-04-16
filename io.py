#i/o 
import re

def fileio( filename ):
	text= None
	with open(filename) as file:
	    text=file.read()

	sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)

	print (sentences)
	retArray = flipFlopped(sentences)

	print retArray



def stdio( filename ):
	return

	# open the file
	# put it into a list of setneces 

	# retArray = flipFlopped(sentenceArray)


	# print retArray

fileio("test.txt")