from src.services import dial, get_lead_phone_number_to_dial
from .lead_call import PendingLeadCall, StartedLeadCall, FailedLeadCall, CompletedLeadCall
import pdb

class PowerDialer:
    DIAL_RATIO = 2

    def __init__(self, agent_id: str, repository):
        self.agent_id     = agent_id
        self.repository   = repository

    def on_agent_login(self):
       [self.__get_lead_and_dial__() for call_number in range(PowerDialer.DIAL_RATIO)]
       self.__log__("agent {} login".format(self.agent_id))

    def on_agent_logout(self):
        agent_leads = self.repository.find_leads_started_by_agent(self.agent_id)

        # This should actually publish an event so that we can end calls
        # For this assignment purpose we will just directly end call
        [self.on_call_ended(phone_number) for phone_number in agent_leads]
        self.__log__("agent {} logout".format(self.agent_id))

    def on_call_started(self, lead_phone_number: str):
        with self.repository.lock(lead_phone_number) as lock_id:
            if lock_id == None:
                self.__log__("on_call_started: lock not acquired for agent {} phone {}".format(self.agent_id, lead_phone_number))
                return

            previous_lead = self.repository.find_lead(lead_phone_number)

            if previous_lead == None:
                previous_lead = PendingLeadCall(self.agent_id, lead_phone_number)

            if previous_lead.transition_to("started") == StartedLeadCall(self.agent_id, lead_phone_number):
                self.repository.update_lead_started(self.agent_id, lead_phone_number)
                self.__log__("agent {} - call started {}".format(lead_phone_number, self.agent_id))

    def on_call_failed(self, lead_phone_number: str):
        with self.repository.lock(lead_phone_number) as lock_id:
            if lock_id == None:
                self.__log__("on_call_failed: lock not acquired for agent {} phone {}".format(self.agent_id, lead_phone_number))
                return

            previous_lead = self.repository.find_lead(lead_phone_number)

            if previous_lead.transition_to("failed") == FailedLeadCall(self.agent_id, lead_phone_number):
                self.repository.update_lead_fail(lead_phone_number)
                self.__get_lead_and_dial__()
                self.__log__("agent {} - call failed {}".format(lead_phone_number, self.agent_id))

    def on_call_ended(self, lead_phone_number: str):
        with self.repository.lock(lead_phone_number) as lock_id:
            if lock_id == None:
                self.__log__("on_call_ended: lock not acquired for agent {} phone {}".format(self.agent_id, lead_phone_number))
                return

            previous_lead = self.repository.find_lead(lead_phone_number)

            if previous_lead.transition_to("completed") == CompletedLeadCall(self.agent_id, lead_phone_number):
                self.repository.update_lead_complete(lead_phone_number)
                self.__get_lead_and_dial__()
                self.__log__("agent {} - call ended {}".format(lead_phone_number, self.agent_id))

    def __get_lead_and_dial__(self):
        phone_number = get_lead_phone_number_to_dial()
        if(phone_number != None): dial(self.agent_id, phone_number)

    def __log__(self, message):
        """
        Dummy log. Should eventually push to Kafka, kinesis, s3...
        """
        print(message)
