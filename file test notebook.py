!pip3 install kfp

########################################################################################################################

import kfp
import kubernetes

########################################################################################################################

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
        "image": "docker.io/rawkintrevo/spark-file-test:0.0.17",
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
            "instances": 2,
            "memory": "512m"
        },
        "labels": {
            "version": "2.4.5"
        },

    }
}

########################################################################################################################


@kfp.dsl.pipeline(
    name="Covid DICOM Pipe v2",
    description="Create Basis Vectors for Lung Images"
)
def covid_dicom_pipeline():
    rop = kfp.dsl.ResourceOp(
        name="calculate-basis-vectors",
        k8s_resource=container_manifest,
        action="create",
        success_condition="status.applicationState.state == COMPLETED"
    )

kfp.compiler.Compiler().compile(covid_dicom_pipeline,"dicom-pipeline-2.zip")
client = kfp.Client()
########################################################################################################################

my_experiment = client.create_experiment(name='my-experiments')
my_run = client.run_pipeline(my_experiment.id, 'my-run1', 'dicom-pipeline-2.zip')
