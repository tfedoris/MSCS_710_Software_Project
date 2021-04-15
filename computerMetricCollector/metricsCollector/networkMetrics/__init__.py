import pandas as pd
import psutil
from datetime import datetime


class NetworkMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format, table):
        self.logger = logger
        self.machine_id = machine_id,
        self.metrics = metrics
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.store_table = table

    def fetch_metrics(self):
        network_card_io = psutil.net_io_counters(pernic=True)
        self.logger.info("Start fetching for network metrics")
        for card in network_card_io.keys():
            self.logger.debug("Fetching for network metrics for network interface: " + card)
            io = network_card_io.get(card)
            metrics = {
                "MachineId": self.machine_id,
                "EntryDatetime": datetime.now().strftime(self.datetime_format),
                "NetworkInterface": card,
                "ByteSend": io.bytes_sent,
                "ByteReceived": io.bytes_recv,
                "ErrorByteReceived": io.errin,
                "ErrorByteSend": io.errout,
                "PacketSend": io.packets_sent,
                "PacketReceived": io.packets_recv,
                "PacketReceivedDrop": io.dropin,
                "PacketSendDrop": io.dropout
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
        self.logger.info("End fetching for network metrics")

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for network metrics")
        return self.metrics_df
