
from os import mkdir, path
from requests import get



#10 (512x438 0.68 1.00)
"https://static.raioss.com/coronacases/case010/IM-0001-0059.dcm" # -> 106 Subj is facing left
"https://static.raioss.com/coronacases/case010/IM-0002-0001.dcm" # -> 58 Front to back
"https://static.raioss.com/coronacases/case010/ser204img00001.dcm" # -> 301 Top progresses down (512x512 1.00 1.00)

# pt1 (512x438 0.68 1.00)
"https://static.raioss.com/coronacases/case001/coronacases_001_002.dcm" # -> 346 1->301 are axialdown, 302->346 coronal to back
"https://static.raioss.com/coronacases/case001/398.dcm" # -> 454 sagittalview

#pt2 (512x438 0.68 1.50):
"https://static.raioss.com/coronacases/case002/761.dcm" # 655 -> 755 coronal
"https://static.raioss.com/coronacases/case002/coronacases_002_002.dcm" # -> 006 sagittal
"https://static.raioss.com/coronacases/case002/coronacases_002_038.dcm" #(512x512 0.68 x 1.50) axial

#pt3: (512x512 1.50 1.50):
"https://static.raioss.com/coronacases/case003/ser203img00002.dcm" # -> 200 (512x512 1.50 1.50)
"https://static.raioss.com/coronacases/case003/IM-0002-0002.dcm" # -> 76 (512x406 0.74 x 1.50)
"https://static.raioss.com/coronacases/case003/IM-0001-0077.dcm" # 142 (512x406 0.74 x 1.50)


#pt4 (512x440 0.68 1.00):
"https://static.raioss.com/coronacases/case004/IM-0001-0317.dcm" #-> 366 sagittal
"https://static.raioss.com/coronacases/case004/IM-0002-0001.dcm" # -> # 51 coronal
"https://static.raioss.com/coronacases/case004/ser204img00002.dcm" # -> 301 (512x512 1.00 1.00) axial


#pt5 :
"https://static.raioss.com/coronacases/case005/ser204img00002.dcm" # -> 301 (512x512 1.00 1.00) axial
"https://static.raioss.com/coronacases/case005/IM-0002-0052.dcm" # -> 121 (512x440 0.68 x 1.00) sagittal
"https://static.raioss.com/coronacases/case005/IM-0001-0002.dcm" # -> 50  (512x440 0.68 x 1.00) coronal


#pt 6:
"https://static.raioss.com/coronacases/case006/IM-0001-0065.dcm" # -> 126 sagittal
"https://static.raioss.com/coronacases/case006/IM-0002-0001.dcm" # -> 064 512x418 0.76 1.50 coronal
"https://static.raioss.com/coronacases/case006/ser203img00001.dcm" # -> 213 (512x512 1.50 1.50 axial


# 7 (512x346 - .71mm / 1.00mm )
"https://static.raioss.com/coronacases/case007/IM-0002-0001.dcm" #-> 58 coronal
"https://static.raioss.com/coronacases/case007/IM-0001-0059.dcm" #-> 120 sagittal
"https://static.raioss.com/coronacases/case007/ser203img00001.dcm" # -> 249 (512x512 1.00 1.00( axial


#8
"https://static.raioss.com/coronacases/case008/IM-0002-0062.dcm" # -> 124 Face Left
"https://static.raioss.com/coronacases/case008/ser204img00001.dcm" # -> 301 Top to bottom (512 x 512 1.00 1.00)
"https://static.raioss.com/coronacases/case008/IM-0001-0001.dcm" # -> 61 Front to back

#9
"https://static.raioss.com/coronacases/case009/IM-0002-0001.dcm" # -> 43 Front to back
"https://static.raioss.com/coronacases/case009/IM-0001-0044.dcm" # -> 102 Face left
"https://static.raioss.com/coronacases/case009/ser204img00001.dcm" # -> 256 Top to bottom (512 512 1.00 1.00)

patients = [
{
    "coronal" : {
        "base_url" : "https://static.raioss.com/coronacases/case001/coronacases_001_",
        "start_at" : 302,
        "end_at"   : 346
    },
    "axial"   : {
            "base_url" : "https://static.raioss.com/coronacases/case001/coronacases_001_",
            "start_at" : 1,
            "end_at"   : 301
        },
    "sagittal"  : {
            "base_url" : "https://static.raioss.com/coronacases/case001/",
            "start_at" : 398,
            "end_at"   : 454
        }

}, # patient 1
{
        "coronal" : {
            "base_url" : "https://static.raioss.com/coronacases/case002/",
            "start_at" : 708,
            "end_at"   : 755
        },
            "axial"   : {
                "base_url" : "https://static.raioss.com/coronacases/case002/coronacases_002_",
                "start_at" : 1,
                "end_at"   : 200
            },
            "sagittal"  : {
                "base_url" : "https://static.raioss.com/coronacases/case002/",
                "start_at" : 655,
                "end_at"   : 707
            }

    }, # patient 2
{
        "coronal" : {
            "base_url" : "https://static.raioss.com/coronacases/case003/IM-0002-0",
            "start_at" : 1,
            "end_at"   : 76
        },
            "axial"   : {
                "base_url" : "https://static.raioss.com/coronacases/case003/ser203img00",
                "start_at" : 1,
                "end_at"   : 200
            },
            "sagittal"  : {
                "base_url" : "https://static.raioss.com/coronacases/case003/IM-0001-0",
                "start_at" : 77,
                "end_at"   : 142
            }

    }, # patient 3
{
    "coronal" : {
        "base_url" : "https://static.raioss.com/coronacases/case004/IM-0002-0",
        "start_at" : 1,
        "end_at"   : 51
    },
        "axial"   : {
            "base_url" : "https://static.raioss.com/coronacases/case004/ser204img00",
            "start_at" : 1,
            "end_at"   : 301
        },
        "sagittal"  : {
            "base_url" : "https://static.raioss.com/coronacases/case004/IM-0001-0",
            "start_at" : 317,
            "end_at"   : 366
        }

}, # patient 4
{
        "coronal" : {
            "base_url" : "https://static.raioss.com/coronacases/case005/IM-0001-0",
            "start_at" : 1,
            "end_at"   : 50
        },
            "axial"   : {
                "base_url" : "https://static.raioss.com/coronacases/case005/ser204img00",
                "start_at" : 1,
                "end_at"   : 301
            },
            "sagittal"  : {
                "base_url" : "https://static.raioss.com/coronacases/case005/IM-0002-0",
                "start_at" : 51,
                "end_at"   : 121
            }

    }, # patient 5
{
    "coronal" : {
        "base_url" : "https://static.raioss.com/coronacases/case006/IM-0002-0",
        "start_at" : 1,
        "end_at"   : 64
    },
        "axial"   : {
            "base_url" : "https://static.raioss.com/coronacases/case006/ser203img00",
            "start_at" : 1,
            "end_at"   : 213
        },
        "sagittal"  : {
            "base_url" : "https://static.raioss.com/coronacases/case006/IM-0001-0",
            "start_at" : 65,
            "end_at"   : 126
        }

}, # patient 6
{
    "coronal" : {
            "base_url" : "https://static.raioss.com/coronacases/case007/IM-0002-0",
            "start_at" : 1,
            "end_at"   : 58
        },
         "axial"   : {
                "base_url" : "https://static.raioss.com/coronacases/case007/ser203img00",
                "start_at" : 1,
                "end_at"   : 249
            },
            "sagittal"  : {
                "base_url" : "https://static.raioss.com/coronacases/case007/IM-0001-0",
                "start_at" : 59,
                "end_at"   : 120
            }

    }, # patient 7
{
        "coronal" : {
        "base_url" : "https://static.raioss.com/coronacases/case008/IM-0001-0",
        "start_at" : 1,
        "end_at"   : 61
    },
        "axial"   : {
            "base_url" : "https://static.raioss.com/coronacases/case008/ser204img00",
            "start_at" : 1,
            "end_at"   : 301
        },
        "sagittal"  : {
            "base_url" : "https://static.raioss.com/coronacases/case008/IM-0002-0",
            "start_at" : 62,
            "end_at"   : 124
        }

}, # patient 8
{
        "coronal" : {
            "base_url" : "https://static.raioss.com/coronacases/case009/IM-0002-0",
            "start_at" : 1,
            "end_at"   : 43
        },
            "axial"   : {
                "base_url" : "https://static.raioss.com/coronacases/case009/ser204img00",
                "start_at" : 1,
                "end_at"   : 256
            },
            "sagittal"  : {
                "base_url" : "https://static.raioss.com/coronacases/case009/IM-0001-0",
                "start_at" : 44,
                "end_at"   : 102
            }

    }, # patient 9
{"coronal" :
    { # patient 10
    "base_url" : "https://static.raioss.com/coronacases/case010/ser204img00",
    "start_at" : 1,
    "end_at"   : 301
    },
    "axial"   : {
        "base_url" : "https://static.raioss.com/coronacases/case010/IM-0002-0",
        "start_at" : 1,
        "end_at"   : 58
    },
    "sagittal"  : {
        "base_url" : "https://static.raioss.com/coronacases/case010/IM-0001-0",
        "start_at" : 59,
        "end_at"   : 106
    }
}
]




def safe_mkdir(path):
    try:
        mkdir(path)
        return True
    except FileExistsError:
        print(f"WARNING: Directory '{path}' already exists.")
        return False

def dload_perspective(name, info, base_dir):
    tgt_dir = base_dir + "/" + name
    safe_mkdir(tgt_dir)
    for i in range(info['start_at'], info['end_at'] + 1):
        fname_base = info['base_url'].split("/")[-1]
        if path.exists(f"{tgt_dir}/{fname_base}{str(i).zfill(3)}.dcm"):
            continue
        url = f"{info['base_url']}{str(i).zfill(3)}.dcm"
        r = get(url, allow_redirects=True)
        open(f"{tgt_dir}/{fname_base}{str(i).zfill(3)}.dcm", 'wb').write(r.content)

for i in range(len(patients)):
    pt = patients[i]
    print(f"case {i+1}")
    base_dir = f"data/case0{str(i+1).zfill(2)}"
    safe_mkdir(base_dir)
    for k in pt.keys():
        dload_perspective(k, pt[k], base_dir)

