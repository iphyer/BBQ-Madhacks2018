import numpy as np
import os.path
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot(array, dirPath):
    matplotlib.use('Agg')


    # truth = np.loadtxt(filename, delimiter=',' )
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    im = np.array(Image.open(os.path.join(dirPath, "image")), dtype=np.uint8)
    ax.set_axis_off()
    print("here")

    ax.imshow(im.astype(np.uint8), cmap='gray')
    recList = list()

    color = {
        0 : "red",
        1 : "blue",
        2 : "yellow"
    }
    for element in array:
        print(element)
    # Adding blue rectangle from predict
    for element in array:
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

    # # Adding red rectangle for truth
    # for rect in truth:
    #     recList.append(
    #         patches.Rectangle(
    #             (rect[0], rect[3]),
    #              np.abs(rect[2] - rect[0]),
    #              np.abs(rect[3] - rect[1]),
    #              fill=False,
    #              edgecolor = "red"
    #         )
    #     )

    # plot the graph
    for p in recList:
        ax.add_patch(p)

    plt.plot()
    # plt.show()
    fig.savefig(os.path.join(dirPath, "out.png"), dpi=190, bbox_inches='tight', pad_inches=0)