from ..services import dial, get_lead_phone_number_to_dial

class PowerDialer:
    DIAL_RATIO = 2

    def __init__(self, agent_id: str, repository):
        self.agent_id     = agent_id
        self.repository   = repository

    def on_agent_login(self):
        for call_number in range(PowerDialer.DIAL_RATIO):
            phone_number = get_lead_phone_number_to_dial()

            if(phone_number != None and dial(self.agent_id, phone_number) == True):
                self.repository.update_lead_pending(self.agent_id, phone_number)

    def on_agent_logout(self):
        self.repository.end_agent_lead_calls(self.agent_id)

    def on_call_started(self, lead_phone_number: str):
        self.repository.assign_agent_to_lead(lead_phone_number, self.agent_id)

    def on_call_failed(self, lead_phone_number: str):
        self.repository.fail_lead(lead_phone_number, self.agent_id)
        self.repository.send_back_to_queue(lead_phone_number)

    def on_call_ended(self, lead_phone_number: str):
        self.repository.complete_lead(lead_phone_number)
