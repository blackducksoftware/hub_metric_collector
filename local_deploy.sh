minikube start --vm-driver=virtualbox --memory=12288 --cpus=2
eval $(minikube docker-env)
docker build -t metriccollector ./
kubectl delete -f rc.yaml
kubectl create -f rc.yaml
kill $(ps | grep -v grep | grep 8080 | cut -f2 -d ' ')
kill $(ps | grep -v grep | grep 9090 | cut -f2 -d ' ')
sleep 15
PODNAME=$(kubectl get pods | grep demo.*Running | cut -f1 -d ' ')
nohup kubectl port-forward $PODNAME 8080:8080 > python.log &
nohup kubectl port-forward $PODNAME 9090:9090 > prometheus.log &
echo "Started"