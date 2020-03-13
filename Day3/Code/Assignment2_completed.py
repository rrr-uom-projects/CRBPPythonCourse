from scipy.ndimage import interpolation, rotate
from scipy.optimize import minimize, basinhopping, brute, differential_evolution
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
from scipy import misc
import numpy as np
import dicom

lung1 = misc.imread("lungs.jpg", flatten=True)
lung2 = misc.imread("lungs2.jpg", flatten=True)


print(lung1.shape, lung2.shape)





# Now attempt to crop out only the part of the image containing the tumour
fig2 = plt.figure(2)

ax = fig2.add_subplot(111)

thePlot = ax.imshow(lung1, cmap="Greys_r")

origin = (lung1.shape[0]/2, lung1.shape[1]/2)
print(origin)

rectParams = [origin[0], origin[1], 10, 10]

print(rectParams)

xmin = 450
xsize = 40
ymin = 100
ysize = 30

offset = transforms.ScaledTranslation(-origin[0]/72, -origin[1]/72, fig2.dpi_scale_trans)
aTransform = ax.transData - offset
rect = patches.Rectangle((rectParams[0], rectParams[1]),rectParams[2], rectParams[3],
                        linewidth=1,edgecolor='r',facecolor='none')

ax.add_patch(rect)


global initPos
initPos = None
def onPress(event, rect=rect):
    if event.inaxes == None:
        return
    contains, attr = rect.contains(event)
    if not contains:
        return
    global initPos

    initPos = [rect.get_x(), rect.get_y(), event.xdata, event.ydata]

def onMove(event, rect=rect):
    global initPos
    if initPos is None:
        return

    if event.inaxes == None:
        return

    x = initPos[2]
    y = initPos[3]
    dx = event.xdata - initPos[2]
    dy = event.ydata - initPos[3]

    rect.set_x(initPos[0] + dx)
    rect.set_y(initPos[1] + dy)

    rect.figure.canvas.draw()

def onRelease(event, rect=rect):
    global initPos
    initPos = None
    pass

def keyboardInterface(event, rect=rect):
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
    rect.figure.canvas.draw()

cid1 = fig2.canvas.mpl_connect('button_press_event', onPress)
cid2 = fig2.canvas.mpl_connect('motion_notify_event', onMove)
cid3 = fig2.canvas.mpl_connect('button_release_event', onRelease)
cid4 = fig2.canvas.mpl_connect('key_press_event', keyboardInterface)

plt.show()

# Assume we have moved the rectangle to the right bit, now crop that bit and display it

indices = [int(rect.get_x()), int(rect.get_x() + rect.get_width()),
           int(rect.get_y()), int(rect.get_y() + rect.get_height())]
print(rect.get_width())
print(indices)

plt.imshow(lung1, cmap="Greys_r")
plt.figure()
plt.imshow(lung1[indices[2]:indices[3], indices[0]:indices[1]], cmap="Greys_r", interpolation='none')
plt.show()
