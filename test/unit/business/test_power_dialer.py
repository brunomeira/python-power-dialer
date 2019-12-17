import unittest
from unittest import mock
from src.repository import MemoryStorageLead
from src.business.power_dialer import PowerDialer

class TestPowerDialer(unittest.TestCase):
    def setUp(self):
        self.repo = repo = MemoryStorageLead()

    @mock.patch("src.business.power_dialer.dial")
    @mock.patch("src.business.power_dialer.get_lead_phone_number_to_dial")
    def test_on_agent_login(self, mock_lead_phone_number, mock_dial):
        """
        Happy case test.
        """
        mock_lead_phone_number.side_effect = ["111-111-1111", "111-111-1112"]
        power_dialer = PowerDialer("1", self.repo)

        power_dialer.on_agent_login()
        self.assertEqual(mock_dial.call_count, 2)

    def test_on_agent_logout(self):
        """
        Happy case test.
        """
        phone_numbers = ["111-111-1111", "111-111-1112"]
        for phone_number in phone_numbers:
            self.repo.storage[phone_number] = ("1", "in_progress")

        power_dialer = PowerDialer("1", self.repo)
        power_dialer.on_agent_logout()

        for phone_number in phone_numbers:
            self.assertEqual(self.repo.find_lead(phone_number), ("1", "complete"))

    def test_on_call_started(self):
        """
        Happy case test.
        """
        phone_number = "111-111-1111"
        self.repo.storage[phone_number] = (None, "pending")
        power_dialer = PowerDialer("1", self.repo)

        power_dialer.on_call_started(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), ("1", "in_progress"))

    def test_on_call_failed(self):
        """
        Happy case test.
        """
        phone_number = "111-111-1111"
        power_dialer = PowerDialer("1", self.repo)
        self.repo.storage[phone_number] = ("1", "in_progress")

        power_dialer.on_call_failed(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), ("1", "failed"))

    def test_on_call_ended(self):
        """
        Happy case test.
        """
        phone_number = "111-111-1111"
        power_dialer = PowerDialer("1", self.repo)
        self.repo.storage[phone_number] = ("1", "in_progress")

        power_dialer.on_call_ended(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), ("1", "complete"))
