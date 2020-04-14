
from ast import literal_eval

from os import listdir

import matplotlib.pyplot as plt
import numpy as np



def read_mahout_drm(path):
    data = {}
    counter = 0
    parts = [p for p in listdir(path) if p.startswith("part")]
    for p in parts:
        with open(f"{path}/{p}", 'r') as f:
            lines = f.read().split("\n")
            for l in lines[:-1]:
                counter +=1
                t = literal_eval(l)
                arr = np.array([t[1][i] for i in range(len(t[1].keys()))])
                data[t[0]] = arr
    print(f"read {counter} lines from {path}")
    return data


def plot_3d_matrix(img3d, img_shape, ax_aspect, sag_aspect, cor_aspect):
    # plot 3 orthogonal slices
    a1 = plt.subplot(2, 2, 1)
    plt.imshow(img3d[:, :, img_shape[2]//2])
    a1.set_aspect(ax_aspect)

    a2 = plt.subplot(2, 2, 2)
    plt.imshow(img3d[:, img_shape[1]//2, :])
    a2.set_aspect(sag_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(img3d[img_shape[0]//2, :, :].T)
    a3.set_aspect(cor_aspect)
    plt.show(cmap=plt.cm.bone)


drmU = read_mahout_drm("data/drmU")
drmV = read_mahout_drm("data/drmV")

drmU_p5 = np.transpose(np.array([drmU[i] for i in range(len(drmU.keys()))]))
drmV_p5 = np.array([drmV[i] for i in range(len(drmV.keys()))])

with open(f"data/s/part-00000", 'r') as f:
    diags = [float(d) for d in f.read().split('\n') if d !='']

recon = drmU_p5 @ np.diag(diags) @ drmV_p5.transpose()
plot_3d_matrix(recon.transpose().reshape((512,512,301)), (512,512,301), 1.0, 0.810547, 1.2337347494963278)

s_csv = np.genfromtxt('data/s.csv', delimiter=',')
s = s_csv.reshape((512,512,301))

plot_3d_matrix(s, s.shape, 1.0, 0.810547, 1.2337347494963278)
