import pandas as pd
import psutil
from datetime import datetime


class NetworkMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.logger = logger
        self.machine_id = machine_id,
        self.metrics = metrics
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        network_card_io = psutil.net_io_counters(pernic=True)
        for card in network_card_io.keys():
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
            self.metrics_df.append(metrics, ignore_index=True)

    def get_metrics_df(self):
        return self.metrics_df
