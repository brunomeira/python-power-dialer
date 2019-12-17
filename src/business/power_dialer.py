from ..services import dial, get_lead_phone_number_to_dial

class PowerDialer:
    DIAL_RATIO = 2

    def __init__(self, agent_id: str, repository):
        self.agent_id     = agent_id
        self.repository   = repository

    def on_agent_login(self):
        for call_number in range(PowerDialer.DIAL_RATIO):
            phone_number = get_lead_phone_number_to_dial()
            if(phone_number != None): dial(self.agent_id, phone_number)

    def on_agent_logout(self):
        agent_leads = self.repository.find_leads_in_progress_by_agent(self.agent_id)

        # This should actually publish an event so that we can end calls
        # For this assignment purpose we will just directly end call
        [self.on_call_ended(phone_number) for phone_number in agent_leads]

    def on_call_started(self, lead_phone_number: str):
        lock_id = self.repository.grant_lock(lead_phone_number)
        if lock_id == None:
            self.__log__("on_call_started lock failed for agent: {}, lead: {}".format(self.agent_id, lead_phone_number))
            return

        self.repository.update_lead_in_progress(self.agent_id, lead_phone_number)
        self.repository.release_lock(lead_phone_number, lock_id)

    def on_call_failed(self, lead_phone_number: str):
        lock_id = self.repository.grant_lock(lead_phone_number)
        if lock_id == None:
            self.__log__("on_call_failed lock failed for agent: {}, lead: {}".format(self.agent_id, lead_phone_number))
            return

        self.repository.update_lead_fail(lead_phone_number)
        self.repository.release_lock(lead_phone_number, lock_id)

    def on_call_ended(self, lead_phone_number: str):
        lock_id = self.repository.grant_lock(lead_phone_number)
        if lock_id == None:
            self.__log__("on_call_ended lock failed for agent: {}, lead: {}".format(self.agent_id, lead_phone_number))
            return

        self.repository.update_lead_complete(lead_phone_number)
        self.repository.release_lock(lead_phone_number, lock_id)

    def __log__(self, message):
        """
        Just a dummy implementation of log system
        """
        print(message)
