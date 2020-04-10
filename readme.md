
### Quickstart

1. Install Kubeflow on your favorite cloud provider (or locally). 
1. Create a Jupyter Notebook Server.
1. Upload `pipeline/DICOM Images to Basis Vectors Pipe.iynb`


### Docker Files

`rawkintrevo/covid-prep-docim`

- Expects to find DOCIMs in `/data` directory. Reads and converts to 3d matrices, and then vectors.
Vectors written to `/mnt/data/s.csv`.

`rawkintrevo/covid-basis-vectors`

- Conatains "fat" jar that is built with `calculate-basis-vectors/` source. Reads `/data/s.csv` and 
outputs basis vectors and linear combinations at `/data/drmVt.txt` and `/data/drmU.txt`.


### We're all in this together. 

If you would like to collaborate on upcoming works regarding the COVID pandemic, please reach out to
`papers at aboriginal-armadillo dot com`.  