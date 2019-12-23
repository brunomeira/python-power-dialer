import unittest
from unittest import mock
from src.repository import MemoryStorageLead
from src.business.power_dialer import PowerDialer
from src.business.lead_call import PendingLeadCall, CompletedLeadCall, FailedLeadCall, StartedLeadCall

class TestPowerDialer(unittest.TestCase):
    def setUp(self):
        self.repo = repo = MemoryStorageLead(0.2)

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
            self.repo.storage[phone_number] = ("1", "started")

        power_dialer = PowerDialer("1", self.repo)
        power_dialer.on_agent_logout()

        for phone_number in phone_numbers:
            self.assertEqual(self.repo.find_lead(phone_number), CompletedLeadCall("1", phone_number, self.repo))

    def test_on_call_started(self):
        """
        Happy case test.
        """
        phone_number = "111-111-1111"
        self.repo.storage[phone_number] = ("1", "called")
        power_dialer = PowerDialer("1", self.repo)
        self.repo.agent_storage["1"] = ("1", "online")

        power_dialer.on_call_started(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), StartedLeadCall("1", phone_number, self.repo))

    @mock.patch("src.business.power_dialer.dial")
    @mock.patch("src.business.power_dialer.get_lead_phone_number_to_dial")
    def test_on_call_failed(self, mock_lead_phone_number, mock_dial):
        """
        Happy case test.
        """
        mock_lead_phone_number.side_effect = ["111-111-1112"]

        phone_number = "111-111-1111"
        power_dialer = PowerDialer("1", self.repo)
        self.repo.storage[phone_number] = ("1", "started")

        power_dialer.on_call_failed(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), FailedLeadCall("1", phone_number, self.repo))

        self.assertEqual(mock_dial.call_count, 1)

    @mock.patch("src.business.power_dialer.dial")
    @mock.patch("src.business.power_dialer.get_lead_phone_number_to_dial")
    def test_on_call_ended(self, mock_lead_phone_number, mock_dial):
        """
        Happy case test. When agent is still online
        """
        mock_lead_phone_number.side_effect = ["111-111-1112"]
        phone_number = "111-111-1111"
        power_dialer = PowerDialer("1", self.repo)
        self.repo.storage[phone_number] = ("1", "started")
        self.repo.agent_storage["1"] = ("1", "online")

        power_dialer.on_call_ended(phone_number)
        self.assertEqual(self.repo.find_lead(phone_number), CompletedLeadCall("1", phone_number, self.repo))

        self.assertEqual(mock_dial.call_count, 1)
