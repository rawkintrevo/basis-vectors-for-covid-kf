
from ast import literal_eval

from os import listdir

import matplotlib.pyplot as plt
import numpy as np

parts = [p for p in listdir("data/drmU") if p.startswith("part")]

data = {}
for p in parts:
    with open(f"data/drmU/{p}", 'r') as f:
        lines = f.read().split("\n")
        for l in lines[:-1]:
            t = literal_eval(l)
            arr = np.array([t[1][i] for i in range(len(t[1].keys()))]).reshape(512,512)
            data[t[0]] = arr

plt.imshow(data[0], cmap=plt.cm.bone)

plt.imshow(
# data[0] * -0.044481787256680526 + \
# data[1] * 0.37185145741809855 + \
    data[2] * 0.1568130107140469 + \
data[3] * 0.07838640020361534 + \
data[4] * 0.010366302365766186, cmap=plt.cm.bone)

plt.show()
