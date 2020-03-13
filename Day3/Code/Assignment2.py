# In this assignment, we will take the automatic registration techniques from
# assignment1, and use them to register images from two time points in the
# treatment of a lung cancer patient. You will then apply some of the image
# processing techniques you learned yesterday to extract a tumour shrinkage
# measurement.

# Everything should be here - you may want to change the optimizations imported
from scipy.ndimage import interpolation, rotate
from scipy.optimize import minimize, basinhopping, brute, differential_evolution
import matplotlib.pyplot as plt
from scipy import misc
import numpy as np
import dicom


# load the two images from DICOM files
lung_time1 =
lung_time2 =


# Here, paste in your automatic registration code


# Here, paste in the code you wrote yesterday to do thresholding
