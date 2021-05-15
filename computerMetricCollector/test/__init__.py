import os
import unittest
import sys
from Cryptodome.PublicKey import RSA
from computerMetricCollector.config import import_config
from computerMetricCollector.test.crypto import read_key
from computerMetricCollector.test.TestCase.TestCom import ComTest
from computerMetricCollector.test.TestCase.TestCPU import CPUTest
from computerMetricCollector.test.TestCase.TestDisk import DiskTest
from computerMetricCollector.test.TestCase.TestDiskIO import DiskIOTest
from computerMetricCollector.test.TestCase.TestMemory import MemoryTest
from computerMetricCollector.test.TestCase.TestNetwork import NetworkTest
from computerMetricCollector.test.TestCase.TestProcess import ProcessTest
from computerMetricCollector.test.TestCase.LoggerTest import set_logger


class TestMiscellaneous(unittest.TestCase):
    if getattr(sys, 'frozen', True):
        root_dir = os.path.dirname(os.path.dirname(sys.executable))
    else:
        root_dir = os.path.dirname(__file__)
    settings = import_config(root_dir)

    def test_logger(self):
        level = "ERROR"
        self.assertLogs(set_logger("DEBUG"), "DEBUG")
        self.assertLogs(set_logger("INFO"), "INFO")
        self.assertLogs(set_logger("WARNING"), "WARNING")
        self.assertLogs(set_logger("ERROR"), "ERROR")
        self.assertLogs(set_logger("FATAL"), "FATAL")

    def test_key(self):
        bits = 2048
        key = RSA.generate(bits)
        encrypt_key = key.publickey().export_key()
        dir_name = os.path.dirname(os.path.dirname(__file__))
        encrypt_key_file = dir_name + TestMiscellaneous.settings.get("encryption_key_file")
        public_key = read_key(encrypt_key_file)
        self.assertEqual(len(encrypt_key), len(public_key))


if __name__ == "__main__":
    test_classes = [TestMiscellaneous, ComTest, CPUTest, DiskTest, DiskIOTest, MemoryTest, NetworkTest, ProcessTest]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
    suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(suite)
