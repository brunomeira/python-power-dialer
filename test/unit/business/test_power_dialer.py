import unittest
from src.repository import MemoryStorageLead
from src.business import PowerDialer

class TestPowerDialer(unittest.TestCase):
    def test_on_agent_login(self):
        repo = MemoryStorageLead()
        power_dialer = PowerDialer("1", repo)

        self.assertEqual(len(repo.storage),  0)

        power_dialer.on_agent_login()

        self.assertEqual(len(repo.storage),  2)

    def test_on_agent_logout(self):
        self.assertTrue(True)

    def test_on_call_started(self):
        self.assertTrue(True)

    def test_on_call_failed(self):
        self.assertTrue(True)

    def test_on_call_ended(self):
        self.assertTrue(True)

