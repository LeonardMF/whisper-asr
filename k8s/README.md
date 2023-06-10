# Deploy in Kubernetes

    $ cd k8s

## Requirements

* kubeclt:

    $ brew install kubectl

* Cluster: Checkout [InitK8sOnAWS](../docs/manuals/InitK8sOnAWS.md) for more informations


## Set Cluster

Einrichten eines bestehenden Clusters:

   $ kubectl config set-cluster aws8 --server=https://<server-url>

Herunterladen der Cluster-Konfiguration aus Rancher und diese dann in ./kube/config integrieren.


## Create Namespace

Create namepace `speaker` and use it as default:

    $ kubectl create namespace speaker

In case something went wrong, delete Namespace:

    $ kubectl delete namespace speaker


## Local ASR

2. Apply deployment for local ASR:

        $ kubectl apply -f whisper-asr-deployment.yaml -n speaker
        $ kubectl apply -f whisper-asr-service.yaml -n speaker
        ($ kubectl rollout restart deployment/whisper-asr)

