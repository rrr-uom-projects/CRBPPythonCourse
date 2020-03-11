'''
Basic Python: Assignment 1
In this script, you have to fill in the missing code (or fix buggy code) to do some basic programming tasks. The idea is you should be able to finish these pretty quickly, 
and get an idea for how python works.

Task 1:
    In this directory is a file called "Files.txt". It contains a list of file names, each of which is contained in the directory "files". 
    A few files are missing because a cat walked over the keyboard during the file copy procedue. Which files are missing?
Task 2:
    Load the data from the files that are available so that the value inside each file can be quickly found from an integer file ID key. 
    The values are floating point numbers.
Task 3:
    Produce a histogram of the data. Play around with the number of bins until it looks nice. 
    Try some of the other options like normalisation. Label your axes!
'''

#
#       TASK 1
#

# You need to get a list of the files in the directory "files"
# You then need to compare it against a list generated from the "Files.txt" file.
# Every pair of students has a unique set of files!
# You will need a library to list the files in the directory


# Here, import a library to list the files:
import os

# Open the file containing the list of patients and read it into a list, one line at a time

expectedFiles = [] # Start with an empty list

# This is a handy way to make sure the file is closed when you're done with it.
# For reference, the open command takes two arguments, a file name and an 'open mode' which may be 'r', 'w' or 'a' 
# Thise mean 'r'ead, 'w'rite and 'a'ppend
with open("Files.txt", 'r') as fileList:
    for line in fileList:
        expectedFiles.append(line.strip())

    
# Now you have a list of files read from the file, you just need to work out which ones are missing.
# First of all, get a list of files in the directory (using a library function)

actualFiles = os.listdir("files/")# Simple function goes here!

# Now you have two lists, you can compare them to find which files are not in the directory

missingFiles = []
for aFile in expectedFiles:
    if aFile in actualFiles: # I don't think there's a better way...
        continue
    missingFiles.append(aFile)
    
print(missingFiles)


#
#       TASK 2
#

# Now you have two lists, you can compare them to find which files are not in the directory

# Now you have your file list, you can loop over it to load them
# Think about which data structure is appropriate to meet the goal of the task
# Bonus: this can be done in a single line!

# Hint: Remember that the file names are just strings, and strings have some methods you may be able to use...
# Hint: Look at the code used to read files in the previous task - you could repurpose that...
# Hint: Remember that you can change a string into an integer by calling int() on it (provided it is all numbers).

filesDict = {}
# you will need a for loop to go over the actualFiles list
for aFile in actualFiles:
    with open("files/" + aFile, 'r') as theFile:
        filesDict[int(aFile.split('.')[0])] = float(theFile.read())
    

# One liner version

filesDictOneLine = {int(aFile.split('.')[0]) : float(open("files/" + aFile, 'r').read()) for aFile in actualFiles}

print(filesDictOneLine[712687619], filesDict[712687619])
    
#
#       TASK 3
#

# You will need to import a library to produce the histogram.
# Check the documentation to see which functions you need, and what arguments they take.

# Import a library
import matplotlib.pyplot as plt # Should be obvious which one I mean!

# Now create the histogram 
# There are loads of things to play with in plotting - have a go with some of them here (e.g. normalisation, colours, etc):
plt.hist(filesDict.values(), bins=10, normed=True)

# Label the axes!
plt.xlabel("Number")
plt.ylabel("Frequency ")

plt.show()