from scipy.optimize import minimize, basinhopping, brute, differential_evolution
from scipy.ndimage import interpolation
import matplotlib.pyplot as plt
from scipy import misc
import numpy as np
import pydicom as dicom



# Instructions:
# Try to work on one step at a time, and keep your code between the instructions for each step.
# I have added a few exit() calls at the end of each step. These will stop python from executing
# everything after the line they are on, so that the skeleton code doesn't cause you any trouble.
# As you finish a step, delete the exit() at the bottom of it to move on to the next step


# Step 1: Load the four lung images from their DICOM files:
# The file names are IMG-0004-0000N.dcm where N is between 1 and 4
# Hint: the function you need is read_file in the dicom module
# Hint: you need to get the pixel array from the dicom object
# Hint: To make life easier, declare all the images global

global lung_1
global lung_2
global lung_3
global lung_4
lungs_1 = dicom.read_file("IMG-0004-00001.dcm").pixel_array
lungs_2 = dicom.read_file("IMG-0004-00002.dcm").pixel_array
lungs_3 = dicom.read_file("IMG-0004-00003.dcm").pixel_array
lungs_4 = dicom.read_file("IMG-0004-00004.dcm").pixel_array

# Now visualise one of the images to make sure it loaded okay
# Hint: this is just a quick check, should be doable in 2 lines!
plt.imshow(lungs_1, cmap="Greys_r")
plt.show()



# Step 2: Modify your code from yesterday to anable automatic registration
# To enable automatic registration, you will need to return a cost function from
# your shiftImages function. You will therefore need to write a second function
# that returns a shifted image so you can work with it later.
# Hint: copy your shiftImages() and cost functions here, then tweak them.
# Hint: Because of how the optimisers work, you will need a second function that
# returns a shifted image.

def costFunction(image1, image2):
    """
    Return the sum of square differences
    """
    return np.mean((image1 - image2)**2)

def shiftImages(shifts, image1, image2):
    """
    This function interpolates the image into its shifted position.
    """
    UD, LR = shifts

    image2 = interpolation.shift(image2, (UD,LR), mode='nearest', order=1)

    # calculate the cost function now
    cf = costFunction(image1, image2)
    return cf

def shiftImagesForPlot(shifts, image):
    """
    This function interpolates the image into its shifted position.
    """
    UD, LR = shifts

    image = interpolation.shift(image, (UD,LR), mode='nearest', order=1)
    return image



# Step 3: Now we can implement an automatic optimiser. The brute force algorithm
# is a good one to start with.
# Hint: Identify which function you want to minimise
# Hint: the brute force optimiser takes parameter limits in a tuple of tuples
# documentation: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html



res1 = brute(shiftImages, ((-100, 100),(-100, 100)), args=(lungs_1, lungs_2))
res2 = brute(shiftImages, ((-100, 100),(-100, 100)), args=(lungs_1, lungs_3))
res3 = brute(shiftImages, ((-100, 100),(-100, 100)), args=(lungs_1, lungs_4))
print(res1, res2, res3)


# Step 4: The automatic registration will return a shift that it thinks best registers the images.
# Use your shift function to apply the registration, then visualise the result on a
# green/purple plot. Does it look okay?
# Hint: re-use some of the code from yesterday

lungs_2_registered = shiftImagesForPlot(res1, lungs_2)
lungs_3_registered = shiftImagesForPlot(res2, lungs_3)
lungs_4_registered = shiftImagesForPlot(res3, lungs_4)
#
# plt.imshow(lungs_1, cmap="Greens_r", alpha=0.5)
# plt.imshow(test, cmap="Purples_r", alpha=0.5)
# plt.show()

# Step 5: Below is some code to implement a clipbox you can use to select the region of
# image that contains the tumour for further analysis. You need to link up the event
# handlers with the right events so it will work.

# Import the bit of matplotlib that can draw rectangles
import matplotlib.patches as patches

# Create a new figure
fig2 = plt.figure(2)
ax = fig2.add_subplot(111)# Stick a subplot into the figure
thePlot = ax.imshow(lungs_1, cmap="Greys_r") # Display the fixed image (your image name may be different)

# Start with a box drawn in the centre of the image
origin = (lungs_1.shape[0]/2, lungs_1.shape[1]/2)
rectParams = [origin[0], origin[1], 10, 10]

# Draw a rectangle in the image

global rect
rect = patches.Rectangle((rectParams[1], rectParams[0]),rectParams[2], rectParams[3],linewidth=1, edgecolor='r',facecolor='none')

ax.add_patch(rect)

# Event handlers for the clipbox
global initPos
initPos = None



def onPress(event):
    """
    This function is called when you press a mouse button inside the figure window
    """
    global rect
    if event.inaxes == None:
        return# Ignore clicks outside the axes
    contains, attr = rect.contains(event)
    if not contains:
        return# Ignore clicks outside the rectangle

    global initPos # Grab the global variable to update it
    initPos = [rect.get_x(), rect.get_y(), event.xdata, event.ydata]

def onMove(event):
    """
    This function is called when you move the mouse inside the figure window
    """
    global initPos
    global rect
    if initPos is None:
        return# If you haven't clicked recently, we ignore the event

    if event.inaxes == None:
        return# ignore movement outside the axes

    x = initPos[2]
    y = initPos[3]
    dx = event.xdata - initPos[2]
    dy = event.ydata - initPos[3]
                                    # This code does the actual move of the rectangle
    rect.set_x(initPos[0] + dx)
    rect.set_y(initPos[1] + dy)

    rect.figure.canvas.draw()

def onRelease(event):
    """
    This function is called whenever a mouse button is released inside the figure window
    """
    global initPos
    initPos = None # Reset the position ready for next click

def keyboardInterface(event):
    """
    This function handles the keyboard interface. It is used to change the size of the
    rectangle.
    """
    global rect
    if event.key == "right":
        # Make the rectangle wider
        w0 = rect.get_width()
        rect.set_width(w0 + 1)
    elif event.key == "left":
        # Make the rectangle narrower
        w0 = rect.get_width()
        rect.set_width(w0 - 1)
    elif event.key == "up":
        # Make the rectangle shorter
        h0 = rect.get_height()
        rect.set_height(h0 - 1)
    elif event.key == "down":
        # Make the rectangle taller
        h0 = rect.get_height()
        rect.set_height(h0 + 1)
################################################################################
# The functions below here will need to be changed for use on Windows!
    elif event.key == "cmd+right":
        # Make the rectangle wider - faster
        w0 = rect.get_width()
        rect.set_width(w0 + 10)
    elif event.key == "cmd+left":
        # Make the rectangle narrower - faster
        w0 = rect.get_width()
        rect.set_width(w0 - 10)
    elif event.key == "cmd+up":
        # Make the rectangle shorter - faster
        h0 = rect.get_height()
        rect.set_height(h0 - 10)
    elif event.key == "cmd+down":
        # Make the rectangle taller - faster
        h0 = rect.get_height()
        rect.set_height(h0 + 10)
################################################################################
# Catch user pressing enter to quit
    elif event.key == "enter":
      plt.close()
      return ## to avoid error on drawing to nonexistent canvas?

    rect.figure.canvas.draw()# update the plot window

cid1 = fig2.canvas.mpl_connect('button_press_event', onPress)
cid2 = fig2.canvas.mpl_connect('motion_notify_event', onMove)
cid3 = fig2.canvas.mpl_connect('button_release_event', onRelease)
cid4 = fig2.canvas.mpl_connect('key_press_event', keyboardInterface)

plt.show()



indices = [int(rect.get_y()), int(rect.get_y() + rect.get_height()), int(rect.get_x()), int(rect.get_x() + rect.get_width())]
print(indices)



# Step 6: You should now have all four images registered in the same location, and a set of image indices
# that crop out just the region you're interested in. Use image processing tecniques to extract
# the volume of thr tumour in each image
# Hint: Start by extracting the volume in just the first image
# Hint: Any technique you think will work is fair game!
# Hint: Maybe looking at a histogram of the image vaues would be helpful?

baselineTumourRegion = lungs_1[indices[0]:indices[1], indices[2]:indices[3]]
day5TumourRegion = lungs_2_registered[indices[0]:indices[1], indices[2]:indices[3]]
day10TumourRegion = lungs_3_registered[indices[0]:indices[1], indices[2]:indices[3]]
day15TumourRegion = lungs_4_registered[indices[0]:indices[1], indices[2]:indices[3]]

subregionsList = [baselineTumourRegion, day5TumourRegion, day10TumourRegion, day15TumourRegion]




means = [np.mean(reg) for reg in subregionsList]


plt.hist(baselineTumourRegion.flatten(), label="Baseline")
plt.hist(day5TumourRegion.flatten(), label="5 days", alpha=0.25)
plt.hist(day10TumourRegion.flatten(), label="10 days", alpha=0.25)
plt.hist(day15TumourRegion.flatten(), label="15 days", alpha=0.25)
plt.legend(loc='best')
plt.show()


times = np.arange(0, 4)*5
plt.plot(times, means)
plt.show()

threshold = 40

thresholdedImages = [np.sum(np.where(reg > threshold)) for reg in subregionsList]

plt.plot(times, thresholdedImages)
plt.show()



# Step 7: Now you have four measurements of tumour volume, plot a graph of tumour shrinkage over time
# from your data. Assume the images are taken 5 days apart, and label your axes accordingly.
# Save the plot as a .png image
