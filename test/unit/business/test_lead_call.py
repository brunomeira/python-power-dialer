import unittest
from src.business.lead_call import PendingLeadCall, CompletedLeadCall, FailedLeadCall, StartedLeadCall

class TestPendingLeadCall(unittest.TestCase):
    def setUp(self):
        self.agent_id = "1"
        self.phone_number = "111-111-1111"
        self.lead_call = PendingLeadCall(self.agent_id, self.phone_number)

    def test_on_call_started(self):
        result = self.lead_call.transition_to("started")
        expected_result = StartedLeadCall(self.agent_id, self.phone_number)
        self.assertEqual(result, expected_result)

    def test_on_call_failed(self):
        error_message = "Transition from pending to failed is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("failed")

        self.assertTrue(error_message in str(context.exception))

    def test_on_call_completed(self):
        error_message = "Transition from pending to completed is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("completed")

        self.assertTrue(error_message in str(context.exception))

    def test_when_same_state(self):
        result = self.lead_call.transition_to("pending")
        self.assertEqual(result, result)

class TestStartedCallLead(unittest.TestCase):
    def setUp(self):
        self.agent_id = "1"
        self.phone_number = "111-111-1111"
        self.lead_call = StartedLeadCall(self.agent_id, self.phone_number)

    def test_on_call_started(self):
        result = self.lead_call.transition_to("started")
        self.assertEqual(result, result)

    def test_on_call_failed(self):
        result = self.lead_call.transition_to("failed")
        expected_result = FailedLeadCall(self.agent_id, self.phone_number)
        self.assertEqual(result, expected_result)

    def test_on_call_completed(self):
        result = self.lead_call.transition_to("completed")
        expected_result = CompletedLeadCall(self.agent_id, self.phone_number)
        self.assertEqual(result, expected_result)

class TestCompletedCallLead(unittest.TestCase):
    def setUp(self):
        self.agent_id = "1"
        self.phone_number = "111-111-1111"
        self.lead_call = CompletedLeadCall(self.agent_id, self.phone_number)

    def test_on_call_started(self):
        error_message = "Transition from completed to started is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("started")

        self.assertTrue(error_message in str(context.exception))

    def test_on_call_failed(self):
        error_message = "Transition from completed to failed is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("failed")

        self.assertTrue(error_message in str(context.exception))

    def test_on_call_completed(self):
        result = self.lead_call.transition_to("completed")
        self.assertEqual(result, result)

class TestFailedCallLead(unittest.TestCase):
    def setUp(self):
        self.agent_id = "1"
        self.phone_number = "111-111-1111"
        self.lead_call = FailedLeadCall(self.agent_id, self.phone_number)

    def test_on_call_started(self):
        error_message = "Transition from failed to started is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("started")

        self.assertTrue(error_message in str(context.exception))

    def test_on_call_completed(self):
        error_message = "Transition from failed to completed is invalid"
        with self.assertRaises(Exception) as context:
            result = self.lead_call.transition_to("completed")

        self.assertTrue(error_message in str(context.exception))

    def test_on_call_failed(self):
        result = self.lead_call.transition_to("failed")
        self.assertEqual(result, result)
