from .processMetrics import ProcessMetricCollector


class MetricsCollector:
    def __init__(self, logger, all_metrics):
        self.collectors = []
        process_collector = ProcessMetricCollector(logger, all_metrics.get("process_metrics"))
        self.collectors.append(process_collector)

    def collect_metrics(self):
        for collector in self.collectors:
            collector.fetch_metrics()
            collector.fetch_statics()
