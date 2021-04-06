from .ProcessMetrics import ProcessMetricCollector


class MetricsCollector:
    def __init__(self, logger, all_metrics):
        self.collectors = []
        self.collectors.append(ProcessMetricCollector(logger, all_metrics.get("process")))

    def collect_metrics(self):
        for collector in self.collectors:
            collector.fetch_metrics()
