!pip3 install kfp

import kfp
import kubernetes



container_manifest = {
    "apiVersion": "sparkoperator.k8s.io/v1beta2",
    "kind": "SparkApplication",
    "metadata": {
        "name": "spark-app",
        "namespace": "kubeflow"
    },
    "spec": {
        "type": "Scala",
        "mode": "cluster",
        "image": "docker.io/rawkintrevo/covid-basis-vectors:0.2.0",
        "imagePullPolicy": "Always",
        "hadoopConf": {
            "fs.gs.project.id": "kubeflow-hacky-hacky",
            "fs.gs.system.bucket": "covid-dicoms",
            "fs.gs.impl" : "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
            "google.cloud.auth.service.account.enable": "true",
            "google.cloud.auth.service.account.json.keyfile": "/mnt/secrets/user-gcp-sa.json",
        },
        "mainClass": "org.rawkintrevo.covid.App",
        "mainApplicationFile": "local:///covid-0.1-jar-with-dependencies.jar", # See the Dockerfile
        "arguments": ["245", "15", "1"],
        "sparkVersion": "2.4.5",
        "restartPolicy": {
            "type": "Never"
        },
        "driver": {
            "cores": 1,
            "secrets": [
                {"name": "user-gcp-sa",
                 "path": "/mnt/secrets",
                 "secretType": "GCPServiceAccount"
                 }
            ],

            "coreLimit": "1200m",
            "memory": "512m",
            "labels": {
                "version": "2.4.5",
            },
            "serviceAccount": "spark-operatoroperator-sa", # also try spark-operatoroperator-sa
        },
        "executor": {
            "cores": 1,
            "secrets": [
                {"name": "user-gcp-sa",
                 "path": "/mnt/secrets",
                 "secretType": "GCPServiceAccount"
                 }
            ],
            "instances": 4,
            "memory": "4084m"
        },
        "labels": {
            "version": "2.4.5"
        },

    }
}
# volumes stripped out of this


# volumes stripped out of this

from kfp.gcp import use_gcp_secret
@kfp.dsl.pipeline(
    name="Covid DICOM Pipe v2",
    description="Create Basis Vectors for Lung Images"
)
def covid_dicom_pipeline():
    vop = kfp.dsl.VolumeOp(
        name="requisition-PVC",
        resource_name="datapvc",
        size="20Gi", #10 Gi blows up...
        modes=kfp.dsl.VOLUME_MODE_RWO
    )
    step1 = kfp.dsl.ContainerOp(
        name="download-dicom",
        image="rawkintrevo/download-dicom:0.0.0.4",
        command=["/run.sh"],
        pvolumes={"/data": vop.volume}
    )
    step2 = kfp.dsl.ContainerOp(
        name="convert-dicoms-to-vectors",
        image="rawkintrevo/covid-prep-dicom:0.9.5",
        arguments=[
            '--bucket_name', "covid-dicoms",
        ],
        command=["python", "/program.py"],
        pvolumes={"/mnt/data": step1.pvolume}
    ).apply(kfp.gcp.use_gcp_secret(secret_name='user-gcp-sa'))
    rop = kfp.dsl.ResourceOp(
        name="calculate-basis-vectors",
        k8s_resource=container_manifest,
        action="create",
        success_condition="status.applicationState.state == COMPLETED"
    ).after(step2)

kfp.compiler.Compiler().compile(covid_dicom_pipeline,"dicom-pipeline-2.zip")
client = kfp.Client()

my_experiment = client.create_experiment(name='my-experiments')
my_run = client.run_pipeline(my_experiment.id, 'my-run1', 'dicom-pipeline-2.zip')

import vtkplotter

from vtkplotter import settings, Plotter

vp = Plotter()

import k3d

vertices = [
    -10, 0, -1,
    10, 0, -1,
    10, 0, 1,
    -10, 0, 1,
]

indices = [
    0, 1, 3,
    1, 2, 3
]

plot = k3d.plot()
plot += k3d.mesh(vertices, indices)
plot.display()

vp = Plotter(screensize=(500,500))

g = vtkplotter.load(vtkplotter.datadir+'timecourse1d/')

from vtkplotter import load
volume = load("/home/rawkintrevo/gits/sidegrifts/basis-vectors-for-covid-kf/data/case001/axial/") #returns a vtkVolume object
show(volume, bg='white')