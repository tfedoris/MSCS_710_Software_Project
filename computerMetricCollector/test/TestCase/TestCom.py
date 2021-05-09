import unittest
import pandas as pd
import os
from computerMetricCollector.crypto import encrypt_data, decrypt_data
from computerMetricCollector.test.crypto import read_key
from computerMetricCollector.config import import_config
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics, get_computer_id
from computerMetricCollector.test.TestCase.LoggerTest import set_logger


class ComTest(unittest.TestCase):
    def setUp(self):
        self.logger = set_logger("DEBUG")
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.settings = import_config(self.root_dir)
        self.date_format = self.settings.get("date_time_format")
        self.meta = self.settings.get("collectors").get("ComputerMetrics")
        self.collector = ComputerMetrics(self.logger, self.meta.get("metrics"),
                                         self.meta.get("metrics_to_encrypt"), self.date_format, self.meta.get("url"))
        self.collector.fetch_metrics()
        self.metrics_df = self.collector.get_metrics_df()
        self.sample_df = pd.read_csv(self.root_dir + "/sample_data/ComputerMetrics.csv",
                                     names=self.meta.get("metrics"))

    def test_com_collector(self):
        match_com_df = self.metrics_df.filter(items=self.meta.get("metrics_to_match"), axis=1)
        sample_df = self.sample_df.drop(["EntryDatetime", "Nonce", "SessionKey"], axis=1)
        pd.testing.assert_frame_equal(match_com_df, sample_df)

    def test_com(self):
        for idx, rec in self.metrics_df.iterrows():
            self.assertRegex(rec["MachineID"], r"^[a-zA-Z0-9-]*$")
            self.assertRegex(rec["MachineName"], r"^[a-zA-Z0-9-]*$")
            self.assertRegex(rec["System"], r"^[a-zA-Z]*$")
            self.assertRegex(rec["Version"], r"^[a-zA-Z0-9.]*$")

    def test_encryption(self):
        raw_metrics_df = self.metrics_df
        encrypt_key = read_key(self.root_dir + self.settings.get("encryption_key_file"))
        encrypt_data(self.collector, encrypt_key)
        encrypted_metrics_df = self.collector.get_metrics_df()
        decrypt_key = read_key(self.root_dir + self.settings.get("decryption_key_file"))
        decrypted_metrics_df = decrypt_data(encrypted_metrics_df, self.meta.get("metrics_to_encrypt"), decrypt_key)
        pd.testing.assert_frame_equal(raw_metrics_df, decrypted_metrics_df)