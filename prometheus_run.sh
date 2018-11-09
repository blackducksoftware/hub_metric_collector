#!/bin/bash

docker run -v $(pwd)/src/etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml -p 9090:9090 prom/prometheus