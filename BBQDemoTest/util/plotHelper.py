import numpy as np
import os.path
from PIL import Image

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker



dpi = 150

def cropImg(info_loc, dirpath):
    # truth = np.loadtxt(filename, delimiter=',' )
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    im = Image.open(os.path.join(dirpath, 'image')).convert('L')

    sz = im.size
    lossBound = 10
    x1 = max(info_loc[0][1] - lossBound, 0)
    y1 = max(info_loc[0][2] - lossBound, 0)
    x2 = min(info_loc[0][3] + lossBound, sz[0]-1)
    y2 = min(info_loc[0][4] + lossBound, sz[1]-1)
    print((x1, y1, x2, y2))
    im = im.crop((x1, y1, x2, y2))
    print(info_loc[1])
    tmpName = "crop_Line"+str(info_loc[1])+".png"
    im.save(os.path.join(dirpath, tmpName))
    return tmpName

def wholeImg(info_loc, dirpath):
    # truth = np.loadtxt(filename, delimiter=',' )
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    im = Image.open(os.path.join(dirpath, "image")).convert('L')

    ax.set_axis_off()
    print("here")
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    ax.margins(0, 0)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())

    ax.imshow(im, cmap='gray')
    recList = list()

    color = {
        0: "red",
        1: "blue",
        2: "yellow"
    }
    # Adding blue rectangle from predict

    p=patches.Rectangle(
        (info_loc[0][1], info_loc[0][2]),
        np.abs(info_loc[0][3] - info_loc[0][1]),
        np.abs(info_loc[0][4] - info_loc[0][2]),
        fill=False,
        edgecolor=color.get(info_loc[0][0]),
        linewidth=2
        )

    # plot the graph
    ax.add_patch(p)

    plt.plot()
    # plt.show()
    tmpName = "whole_Line" + str(info_loc[1])+".png"

    fig.savefig(os.path.join(dirpath, tmpName), dpi=dpi, bbox_inches='tight', pad_inches=0)
    return tmpName


def plotloc(loc_list, dirPath):
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