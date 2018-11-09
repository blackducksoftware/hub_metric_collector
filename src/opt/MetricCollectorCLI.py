import MetricCollector

def main():
  metricCollector = MetricCollector.MetricCollector(MetricCollector.insecure)
  status = metricCollector.execute()
  print metricCollector.output
  return status

exit(main())