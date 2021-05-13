import pandas as pd
import psutil
from datetime import datetime
from computerMetricCollector.metricsCollector import Collector


class NetworkMetrics(Collector):
    def __init__(self, logger, machine_id, metrics, metrics_to_encrypt, datetime_format, url):
        self.is_fetch = False
        self.to_stored = False
        self.logger = logger
        self.machine_id = machine_id,
        if type(self.machine_id) == tuple:
            self.machine_id = str(machine_id)
        self.metrics_to_encrypt = metrics_to_encrypt
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.remote_url = url

    def fetch_metrics(self):
        """
        This function fetch the metrics to be store in the database
        :return:
        """
        network_card_io = psutil.net_io_counters(pernic=True)
        self.logger.info("Start fetching for network metrics")
        for card in network_card_io.keys():
            self.logger.debug("Fetching for network metrics for network interface: " + card)
            io = network_card_io.get(card)
            metrics = {
                "machine_id": self.machine_id,
                "entry_time": datetime.now().strftime(self.datetime_format),
                "network_interface": card,
                "bytes_send": io.bytes_sent,
                "bytes_receive": io.bytes_recv,
                "error_bytes_receive": io.errin,
                "error_bytes_send": io.errout,
                "packet_sent": io.packets_sent,
                "packet_receive": io.packets_recv,
                "packet_receive_drop": io.dropin,
                "packet_send_drop": io.dropout
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
            self.metrics_df = self.metrics_df.reset_index(drop=True)
        self.logger.info("End fetching for network metrics")
        self.is_fetch = True
        self.to_stored = True

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for network metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False
