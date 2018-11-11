import numpy as np
import os.path
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker

dpi = 150

def plotloc(loc_list, dirPath):
    matplotlib.use('Agg')


    # truth = np.loadtxt(filename, delimiter=',' )
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    im = np.array(Image.open(os.path.join(dirPath, "image")), dtype=np.uint8)
    ax.set_axis_off()
    print("here")
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    ax.margins(0, 0)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())


    ax.imshow(im.astype(np.uint8), cmap='gray')
    recList = list()

    color = {
        0 : "red",
        1 : "blue",
        2 : "yellow"
    }
    # Adding blue rectangle from predict
    for element in loc_list:
        rect = element[0]
        recList.append(
            patches.Rectangle(
                (rect[1], rect[2]),
                np.abs(rect[3] - rect[1]),
                np.abs(rect[4] - rect[2]),
                fill=False,
                edgecolor = color.get(rect[0]),
                linewidth=2
            )
        )

    # plot the graph
    for p in recList:
        ax.add_patch(p)

    plt.plot()
    # plt.show()
    fig.savefig(os.path.join(dirPath, "loc.png"), dpi=dpi, bbox_inches='tight', pad_inches=0)


def plotcls(cls_list, dirPath):
    matplotlib.use('Agg')


    # truth = np.loadtxt(filename, delimiter=',' )
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    im = np.array(Image.open(os.path.join(dirPath, "image")), dtype=np.uint8)
    ax.set_axis_off()
    print("here")
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    ax.margins(0, 0)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())


    ax.imshow(im.astype(np.uint8), cmap='gray')
    recList = list()

    # Adding blue rectangle from predict
    for element in cls_list:
        pred = element[0]
        gt = element[2]
        recList.append(
            patches.Rectangle(
                (pred[1], pred[2]),
                np.abs(pred[3] - pred[1]),
                np.abs(pred[4] - pred[2]),
                fill=False,
                edgecolor = 'red',
                linewidth=1
            )
        )

        recList.append(
            patches.Rectangle(
                (gt[1], gt[2]),
                np.abs(gt[3] - gt[1]),
                np.abs(gt[4] - gt[2]),
                fill=False,
                edgecolor = 'blue',
                linewidth=1
            )
        )
    # plot the graph
    for p in recList:
        ax.add_patch(p)

    plt.plot()
    # plt.show()
    fig.savefig(os.path.join(dirPath, "cls.png"), dpi=dpi, bbox_inches='tight', pad_inches=0)