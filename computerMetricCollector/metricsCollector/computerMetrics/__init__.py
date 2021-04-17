import platform
import pandas as pd
import winreg


def get_computer_id(logger):
    logger.info("Getting computer id")
    reg_key = winreg.HKEY_LOCAL_MACHINE
    sub_key = "SOFTWARE\\Microsoft\\Cryptography"
    key_read = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    logger.debug("Read registry key " + str(reg_key))
    logger.debug("Read substitute key " + str(sub_key))
    logger.debug("Read access key " + str(key_read))
    logger.info("Open registry key")
    key = winreg.OpenKey(key=reg_key, sub_key=sub_key, reserved=0, access=key_read)
    logger.info("Query registry key")
    value = winreg.QueryValueEx(key, 'MachineGuid')
    logger.info("Close registry key")
    winreg.CloseKey(key)
    logger.info("End getting computer id")
    return value[0]


class ComputerMetrics:
    def __init__(self, logger, metrics):
        self.is_fetched = False
        self.to_stored = False
        self.logger = logger
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.machine_id = get_computer_id(self.logger)

    def fetch_metrics(self):
        self.logger.info("Is computer metrics fetched: " + str(self.is_fetched))
        if not self.is_fetched:
            self.logger.info("Fetch for computer metrics")
            machine_info = platform.uname()
            metrics = {
                "MachineID": self.machine_id,
                "MachineName": machine_info.node,
                "System": machine_info.system,
                "Version": machine_info.version,
                "MachineType": machine_info.machine
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
            self.is_fetched = True
            self.to_stored = True
        else:
            self.logger.info("No fetch for computer metrics")

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for computer metrics")
        return self.metrics_df
