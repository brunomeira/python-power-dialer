from threading import current_thread
from contextlib import contextmanager
from src.services import dial, get_lead_phone_number_to_dial
from .lead_call import PendingLeadCall, StartedLeadCall, FailedLeadCall, CompletedLeadCall, CalledLeadCall
from .agent import OnlineAgent, OfflineAgent

class PowerDialer:
    DIAL_RATIO = 2

    def __init__(self, agent_id: str, repository):
        self.agent_id     = agent_id
        self.repository   = repository

    def on_agent_login(self):
        with self.repository.lock(self.agent_id) as lock_id:
           self.agent = self.repository.find_agent(self.agent_id)
           new_agent_state = self.agent.transition_to("online")

           if new_agent_state.state == "online":
               for call_number in range(PowerDialer.DIAL_RATIO):
                   phone_number = self.__get_lead_and_dial__()

                   if phone_number is not None:
                       pending_lead_call = PendingLeadCall(self.agent_id, phone_number, self.repository)
                       pending_lead_call.transition_to("called")

               self.__log__("agent {} login".format(self.agent_id))

    def on_agent_logout(self):
        with self.repository.lock(self.agent_id) as lock_id:
           agent = self.repository.find_agent(self.agent_id)
           agent_leads = self.repository.find_leads_started_by_agent(self.agent_id)

           # This should actually publish an event so that we can end calls
           # For this assignment purpose we will just directly end call
           agent = agent.transition_to("offline")

           self.__log__("agent {} logout - leads {}".format(self.agent_id, agent_leads))

           if agent.state == "offline":
               for lead in agent_leads:
                   previous_lead = self.__fetch_lead_state__(lead)
                   new_state = previous_lead.transition_to("completed")
                   self.__log__("agent {} - call ended {}".format(self.agent_id, lead))



    def on_call_started(self, lead_phone_number: str):
        with self.repository.lock(self.agent_id) as lock_id:
            agent = self.repository.find_agent(self.agent_id)

            if(agent.state == "online"):
                previous_lead = self.repository.find_lead(lead_phone_number)

                if previous_lead.state == "pending":
                    previous_lead.agent_id = self.agent_id
                    previous_lead = previous_lead.transition_to("called")

                new_state = previous_lead.transition_to("started")

                if new_state.state == "started":
                    self.__log__("agent {} - call started {}".format(self.agent_id,lead_phone_number))


    def on_call_failed(self, lead_phone_number: str):
        with self.repository.lock(self.agent_id) as lock_id:
            previous_lead = self.repository.find_lead(lead_phone_number)
            new_state = previous_lead.transition_to("failed")

            if new_state.state == "failed":
                self.__get_lead_and_dial__()
                self.__log__("agent {} - call failed {}".format(self.agent_id, lead_phone_number))

    def on_call_ended(self, lead_phone_number: str):
        with self.repository.lock(self.agent_id) as lock_id:
            agent = self.repository.find_agent(self.agent_id)

            previous_lead = self.__fetch_lead_state__(lead_phone_number)
            new_state = previous_lead.transition_to("completed")

            if new_state.state == "completed":
                if(agent is not None and agent.state == "online"):
                    self.__get_lead_and_dial__()
                self.__log__("agent {} - call ended {}".format(self.agent_id, lead_phone_number))

    def __fetch_lead_state__(self, lead_phone_number):
        return self.repository.find_lead(lead_phone_number)

    def __get_lead_and_dial__(self):
        phone_number = get_lead_phone_number_to_dial()
        if(phone_number is not None):
            return dial(self.agent_id, phone_number)

    def __log__(self, message):
        """
        Dummy log. Should eventually push to Kafka, kinesis
        """
        self.repository.add_log(message + " By: " + current_thread().name)
