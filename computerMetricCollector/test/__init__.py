import os
import pandas as pd
import unittest
from Cryptodome.PublicKey import RSA
from computerMetricCollector.CollectoUtils import get_logger, init_collector, persist_local, persist_database
from computerMetricCollector.config import import_config
from computerMetricCollector.crypto import encrypt_data, read_key, decrypt_data
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics, get_computer_id


def set_logger(level):
    log_file = "Test.log"
    rotate_time = "midnight"
    backup_cnt = 10
    logger = get_logger(log_file, level, rotate_time, backup_cnt)
    return logger


class TestCollect(unittest.TestCase):
    logger = set_logger("ERROR")

    def test_logger(self):
        level = "ERROR"
        self.assertLogs(set_logger("DEBUG"), "DEBUG")
        self.assertLogs(set_logger("INFO"), "INFO")
        self.assertLogs(set_logger("WARNING"), "WARNING")
        self.assertLogs(TestCollect.logger, level)
        self.assertLogs(set_logger("FATAL"), "FATAL")

    def test_key(self):
        root_dir = os.path.dirname(__file__)
        settings = import_config(root_dir)
        bits = 2048
        key = RSA.generate(bits)
        encrypt_key = key.publickey().export_key()
        dir_name = os.path.dirname(os.path.dirname(__file__))
        encrypt_key_file = dir_name + settings.get("encryption_key_file")
        public_key = read_key(encrypt_key_file)
        self.assertEqual(len(encrypt_key), len(public_key))

    def test_collector(self):
        root_dir = os.path.dirname(__file__)
        settings = import_config(root_dir)
        collectors_meta = settings.get("collectors")
        datetime_format = settings.get("date_time_format")
        com_meta = collectors_meta.get("ComputerMetrics")
        com_collector = ComputerMetrics(TestCollect.logger, com_meta.get("metrics"),
                                        com_meta.get("metrics_to_encrypt"), datetime_format, com_meta.get("url"))
        com_collector.fetch_metrics()
        com_df = com_collector.get_metrics_df()
        com_df = com_df.filter(items=com_meta.get("metrics_to_match"), axis=1)
        sample_df = pd.read_csv(root_dir + "/sample_data/decrypted_ComputerMetrics.csv", names=com_meta.get("metrics"))
        sample_df = sample_df.drop(["EntryDatetime", "Nonce", "SessionKey"], axis=1)

        pd.testing.assert_frame_equal(com_df, sample_df)
        del collectors_meta["ComputerMetrics"]
        for collector_str in collectors_meta.keys():
            meta = collectors_meta.get(collector_str)
            if len(meta.get("metrics_to_match")) == 0:
                continue
            collector = init_collector(TestCollect.logger, collectors_meta, collector_str, com_collector.machine_id,
                                       datetime_format)
            collector.fetch_metrics()
            metrics_df = collector.get_metrics_df()
            sample_df = pd.read_csv(root_dir + "/sample_data/decrypted_" + collector_str + ".csv",
                                    names=metrics_df.columns)
            metrics_df = metrics_df.filter(items=meta.get("metrics_to_match"), axis=1)
            sample_df = sample_df.filter(items=meta.get("metrics_to_match"), axis=1)
            pd.testing.assert_frame_equal(metrics_df, sample_df, check_dtype=False)

    def test_com_id(self):
        com_id = get_computer_id(TestCollect.logger)
        self.assertRegex(com_id, r"^[a-zA-Z0-9-]*$")

    def test_encryption(self):
        root_dir = os.path.dirname(__file__)
        settings = import_config(root_dir)
        collectors_meta = settings.get("collectors")
        datetime_format = settings.get("date_time_format")
        com_meta = collectors_meta.get("ComputerMetrics")
        com_collector = ComputerMetrics(TestCollect.logger, com_meta.get("metrics"),
                                        com_meta.get("metrics_to_encrypt"), datetime_format, com_meta.get("url"))
        com_collector.fetch_metrics()
        raw_metrics_df = com_collector.get_metrics_df()
        encrypt_key = read_key(root_dir + settings.get("encryption_key_file"))
        encrypt_data(com_collector, encrypt_key)
        encrypted_metrics_df = com_collector.get_metrics_df()
        with open(root_dir + "\\crypto\\ppk\private.pem") as f:
            decrypt_key = f.read()
        decrypted_metrics_df = decrypt_data(encrypted_metrics_df, com_meta.get("metrics_to_encrypt"), decrypt_key)
        pd.testing.assert_frame_equal(raw_metrics_df, decrypted_metrics_df)


if __name__ == "__main__":
    unittest.main()
