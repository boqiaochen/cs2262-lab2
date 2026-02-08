# Lab 2 - Problem 2: Time App

This folder contains a simple Flask app containerized with Docker and deployed to Kubernetes (Minikube).

## Docker (build & run locally)
cd time_app
docker build -t bc3791/sample-time-app:latest .
docker run --rm -p 8080:8080 bc3791/sample-time-app:latest
curl http://localhost:8080/time

## Docker Hub (push)
docker push bc3791/sample-time-app:latest

## Kubernetes (Minikube)
kubectl create deployment sample-time-app --image=docker.io/bc3791/sample-time-app:latest
kubectl expose deployment/sample-time-app --type="NodePort" --port 8080
kubectl get pods
kubectl get services
minikube service sample-time-app --url
# then:
curl http://127.0.0.1:<PORT>/time
