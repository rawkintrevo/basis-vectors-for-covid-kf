
from os import listdir
from scipy.ndimage import zoom

import numpy as np
import pydicom


"""
Params: 
 anatomical_plane: sagittal 
 tgt_length = 301

"""
# Todo Only sagittal right now bc they're all 512x512 - we then set the "length" at 301 with a zoom. however, it
# todo wouldn't be hard to just specify desired dimensions...

tgt_length = 301
plane = "axial"

def create_3d_matrix(path):
    dicoms = [pydicom.dcmread(f"{path}/{f}") for f in listdir(path)]
    slices = [d for d in dicoms if hasattr(d, "SliceLocation")]
    slices = sorted(slices, key=lambda s: s.SliceLocation)
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1]/ps[0]
    sag_aspect = ps[1]/ss
    cor_aspect = ss/ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d

    return {"img3d": img3d, "img_shape": img_shape, "ax_aspect" : ax_aspect, "sag_aspect" : sag_aspect, "cor_aspect" : cor_aspect }



with open("/mnt/data/s.csv", 'w') as f:
    f.write("")

with open("/mnt/data/s.csv", 'a') as f:
    for case in range(1,11):
        print(f"Working on Case {case}")
        m = create_3d_matrix(f"/data/case0{str(case).zfill(2)}/{plane}") # axial is top-
        print(f"Case {case}, {m['img_shape']}")
        if m['img_shape'][2] != tgt_length:
            m['img3d'] = zoom(m['img3d'], (1,1,float(tgt_length)/m["img_shape"][2]))
        tv = ",".join([str(v) for v in m['img3d'].reshape((1,-1))[0]])
        f.write(tv + "\n")
    print("beginning work on 'healthy' cases")
    for pt in listdir("/data/PREM-20090113"):
        for date in listdir(f"/data/PREM-20090113/{pt}"):
            for scan in listdir(f"/data/PREM-20090113/{pt}/{date}"):
                m = create_3d_matrix(f"/data/PREM-20090113/{pt}/{date}/{scan}")
                if m['img_shape'][2] != tgt_length:
                    m['img3d'] = zoom(m['img3d'], (1,1,float(tgt_length)/m["img_shape"][2]))
                tv = ",".join([str(v) for v in m['img3d'].reshape((1,-1))[0]])
                f.write(tv + "\n")

print(f"Job Successful.")
