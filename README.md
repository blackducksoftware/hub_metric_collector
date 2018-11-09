# Docker Hub Monitoring

This is a Training repository for Rob. Jay Vyas assigned a monitoring project to Rob.

This repository contains code for monitoring the number of Hubs that are online and available. 

This contains:

* A Python Docker Container which monitors cluster status
* A Kubernetes Replication controller. It will deploy the Python Docker container, as well as Prometheus. Prometheus will be configured to collect information from the Python Docker Container.

