
from os import listdir
from scipy.ndimage import zoom

import numpy as np
import pydicom

import argparse

parser = argparse.ArgumentParser(description='Process DICOM Images into Vectors.')
parser.add_argument('--input_dir', type=str, default="/mnt/data",
                    help='Directory containing DICOM Images')
parser.add_argument('--output_dir', type=str, default="/data",
                    help='Directory where s.csv (image vectors) will be written to')
parser.add_argument('--min_slice', type=int, default=0,
                    help='Low end of range of slices to create s matrices out of.')
parser.add_argument('--max_slice', type=int, default=301,
                    help='High end of range of slices to create s matrices out of.')

args = parser.parse_args()


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

slice_range = range(args.min_slice, args.max_slice+1)

for i in slice_range:
    with open(f"{args.output_dir}/s.{i}.csv", 'w') as f:
        f.write("")


counter = 0
for case in range(1,11):
    print(f"Working on Case {case}")
    m = create_3d_matrix(f"{args.input_dir}/case0{str(case).zfill(2)}/{plane}") # axial is top-
    print(f"Case {case}, {m['img_shape']}")
    if m['img_shape'][2] != tgt_length:
        m['img3d'] = zoom(m['img3d'], (1,1,float(tgt_length)/m["img_shape"][2]))
    for i in slice_range:
        with open(f"{args.output_dir}/s.{i}.csv", 'a') as f:
            tv = ",".join([str(v) for v in m['img3d'][:,:,i].reshape((1,-1))[0]])
            f.write(tv + "\n")
            counter += 1
print("beginning work on 'healthy' cases")
for topdir in ["PCsub1-20090909", "PCsub2-20090909"]:
    for pt in listdir(f"{args.input_dir}/{topdir}"):
        for date in listdir(f"{args.input_dir}/{topdir}/{pt}"):
            for scan in listdir(f"{args.input_dir}/{topdir}/{pt}/{date}"):
                m = create_3d_matrix(f"{args.input_dir}/{topdir}/{pt}/{date}/{scan}")
                if m['img_shape'][2] != tgt_length:
                    m['img3d'] = zoom(m['img3d'], (1,1,float(tgt_length)/m["img_shape"][2]))
                for i in slice_range:
                    with open(f"{args.output_dir}/s.{i}.csv", 'a') as f:
                        tv = ",".join([str(v) for v in m['img3d'][:,:,i].reshape((1,-1))[0]])
                        f.write(tv + "\n")
                        counter += 1


print(f"Job Successful. {i} image slices written.")
