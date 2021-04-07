import platform


class ComputerMetrics:
    def __init__(self):
        self.is_fetched = False
        self.cache_metrics = {}

    def fetch_metrics(self):
        if not self.is_fetched:
            machine_info = platform.uname()
            self.cache_metrics = {
                "machine_name": machine_info.node,
                "system": machine_info.system,
                "version": machine_info.version,
                "machine_type": machine_info.machine
            }
            self.is_fetched = True
        return self.cache_metrics
