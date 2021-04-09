import platform
import pandas as pd
import winreg


def get_computer_id():
    reg_key = winreg.HKEY_LOCAL_MACHINE
    sub_key = "SOFTWARE\\Microsoft\\Cryptography"
    key_read = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    key = winreg.OpenKey(key=reg_key, sub_key=sub_key, reserved=0, access=key_read)
    value = winreg.QueryValueEx(key, 'MachineGuid')
    winreg.CloseKey(key)
    return value[0]


class ComputerMetrics:
    def __init__(self, logger, metrics):
        self.is_fetched = False
        self.logger = logger
        self.metrics_df = pd.DataFrame(metrics)
        self.machine_id = get_computer_id()

    def fetch_metrics(self):
        if not self.is_fetched:
            machine_info = platform.uname()
            metrics = {
                "MachineID": self.machine_id,
                "MachineName": machine_info.node,
                "System": machine_info.system,
                "Version": machine_info.version,
                "MachineType": machine_info.machine
            }
            self.metrics_df.append(metrics, ignore_index=True)
            self.is_fetched = True

    def get_metrics_df(self):
        return self.metrics_df
