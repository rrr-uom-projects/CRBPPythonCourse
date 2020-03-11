import os
import struct
import tempfile as tf
import numpy as np

import matplotlib.pyplot as plt

# Set up files and directories for assignment 1

N = 1000 # number of files to generate

split = 0.75 # fraction in group 1

N0 = (1.0 - split) * N
N1 = N - N0

# We will use two gaussians to model a distribution
mean0 = 25
sigma0 = 5

mean1 = 55
sigma1 = 10

seed = 198619

seed = struct.unpack('I', os.urandom(4))

np.random.seed(seed)

group1 = np.random.normal(loc=mean0, scale=sigma0, size=N0)
group2 = np.random.normal(loc=mean1, scale=sigma1, size=N1)

# Stick all the data together
alldata = np.hstack((group1, group2))


# Create the directory
try:
    os.mkdir("files")
except OSError:
    pass

# Make some random number ids
IDs = np.random.random_integers(0, high=1000000000, size=N)


# Write the data
for pn, pid in enumerate(IDs):
    with open("files/{0}.txt".format(pid), 'w') as pf:
        pf.write("{0}\n".format(alldata[pn]))

# write the files list
with open("Files.txt", 'w') as fl:
    for pid in IDs:
        fl.write("{0}.txt\n".format(pid))

# Pick a few to delete
todelete = np.random.random_integers(0, high=N, size=3)

print(todelete)
# delete them
for d in todelete:
    os.remove("files/{0}.txt".format(IDs[d]))

dids = [str(IDs[d]) for d in todelete]

# Write the answer down in a files
with open("Seed{0}_answer.txt".format(seed), 'w') as answers:
    answers.write("Files deleted: {0}\n".format(", ".join(dids)))
